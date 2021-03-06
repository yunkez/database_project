from django.shortcuts import render,render_to_response, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.core.context_processors import csrf
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Book,Customer
from .forms import CustomerCreationForm,CustomerChangeForm,BookCreationForm
from django.db import connection
import datetime
import ast
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required(login_url='/login')
def index(request):
    cur = connection.cursor()
    book_list = ""
    author = ""
    publisher = ""
    title = ""
    subject = ""
    orderby = 1
    isManager = request.user.is_superuser
    page_title = "Most Popular Recommendations"
    try:
        cur.execute("SELECT b.*,T.average FROM bookstore_book b,(SELECT book_id, AVG(score) AS average \
            FROM bookstore_feedback GROUP BY book_id) T WHERE b.ISBN=T.book_id UNION SELECT b.*,0 AS average \
        FROM bookstore_book b WHERE b.ISBN NOT IN (SELECT book_id FROM bookstore_feedback) ORDER BY average DESC;")
        columns = [col[0] for col in cur.description]
        book_list = [dict(zip(columns, row)) for row in cur.fetchall()][:10]
    except:
        book_list = ""
    if request.method == 'POST':
        author = request.POST['search_author'] 
        publisher = request.POST['search_publisher'] 
        title = request.POST['search_title'] 
        subject = request.POST['search_subject']
        orderby = request.POST['orderby']
        page_title = "Your Search Results "
        sql ="SELECT b.*,average from (SELECT * FROM bookstore_book where title LIKE '%s' and author LIKE '%s' \
            and publisher LIKE'%s' and subject LIKE '%s') b, (SELECT book_id, AVG(score) AS average FROM \
            bookstore_feedback GROUP BY book_id UNION SELECT ISBN,0 FROM bookstore_book WHERE ISBN NOT IN \
            (SELECT book_id FROM bookstore_feedback)) T WHERE b.ISBN=T.book_id order by %s DESC "%\
        (searchValue(title),searchValue(author),searchValue(publisher),searchValue(subject),orderby)
        cur.execute(sql)
        columns = [col[0] for col in cur.description]
        book_list = [dict(zip(columns, row)) for row in cur.fetchall()]
    paginator = Paginator(book_list, 5)
    page = request.GET.get('page')
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        books = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        books = paginator.page(paginator.num_pages)
    return render(request, 'bookstore/index.html',{'book_list': book_list,'books':books,'author':author,'subject':subject,
            'title':title,'publisher':publisher,'orderby':orderby,'base_template':'base_auth.html',
            'page_title':page_title,'isManager':isManager})

def searchValue(s):
    return "%"+s+"%"

@login_required(login_url='/login')
def detail(request,isbn,count=0,err=0):
    cur = connection.cursor()
    isManager = request.user.is_superuser
    feedback_list=[]

    cur.execute("SELECT * from bookstore_book b WHERE b.ISBN='%s';"%(isbn))
    columns = [col[0] for col in cur.description]
    book = [dict(zip(columns, row)) for row in cur.fetchall()]
    
    cur.execute("SELECT AVG(score) FROM bookstore_feedback where book_id='%s';"%(isbn))
    average = cur.fetchone()[0]
    if average < 0:
        average = 0

    count = int(count)
    sql ="SELECT bf.*,temp.rate,temp.numVotes FROM bookstore_feedback bf join(\
    select r2.rater_id,r2.book_id,r2.rate ,count(*) as numVotes,priority from bookstore_rating r2 join(\
    select r.rater_id,r.book_id,avg(r.rate) as priority from bookstore_rating r group by r.book_id,r.rater_id having r.book_id='%s') as rank\
    where r2.book_id='%s' and rank.rater_id=r2.rater_id group by r2.rate,r2.rater_id,rank.priority) as temp \
    where temp.rater_id = bf.customer_id and bf.book_id = '%s' order by temp.priority desc,rater_id;"%(isbn,isbn,isbn)
    sql2 = "SELECT bf.* from bookstore_feedback bf where bf.customer_id not in (select rater_id from bookstore_rating where book_id='%s') and bf.book_id='%s';"%(isbn,isbn)
    cur.execute(sql)

    name=''
    i = -1
    while (True):
        tmp = cur.fetchone()
        if tmp == None: break
        if(name!=tmp[1]): 
            name = tmp[1]
            i+=1
            if (i>=count and count!=0):
                break;
            feedback_list.append({'customer_id':tmp[1],'book_id':tmp[0],'text':tmp[2],'score':tmp[3],'date':tmp[4],'0':0L,'1':0L,'2':0L})
            feedback_list[i][str(tmp[5])] = tmp[6]
        else:
            feedback_list[i][str(tmp[5])] = tmp[6]
    cur.execute(sql2)
    while (True and (i<count-1 or count==0)):
        tmp = cur.fetchone()
        if tmp == None: break
        feedback_list.append({'customer_id':tmp[1],'book_id':tmp[0],'text':tmp[2],'score':tmp[3],'date':tmp[4],'0':0L,'1':0L,'2':0L})
        i+=1

    return render(request, 'bookstore/index_detail.html',{'book': book[0],'feedback_list':feedback_list,
        'isManager':isManager,'average':average,'base_template':'base_auth.html','error':err})

@login_required(login_url='/login')
def feedback(request):
    cur = connection.cursor()
    text = request.POST['feedback_text']
    ISBN = request.POST['feedback_isbn']
    score = request.POST['feedback_score']
    username = request.user.username
    now=datetime.datetime.now()
    date="%s/%s/%s" % (now.day, now.month, now.year)
    if score != 0 or text.replace(" ", "") != "":
        try:
            sql = "INSERT INTO bookstore_feedback VALUES ('%s','%s','%s','%s','%s')"%\
                    (ISBN,username, text,score,date)
            cur.execute(sql)
        except:
            return redirect(reverse("detail",args=[ISBN,0,5]))
        return redirect(reverse("detail",args=[ISBN,0,6]))
    else:
        return redirect(reverse("detail",args=[ISBN,0,4]))
    

def user_login(request):
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/bookstore')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            return HttpResponse("You have entered wrong username or password.")
    else:
        return render_to_response('bookstore/login.html', {'base_template':'base.html'}, context)

def register(request):
    context = RequestContext(request)
    cur = connection.cursor()
    registered = False
    if request.method == 'POST':
        user_form = CustomerCreationForm(data=request.POST)
        if user_form.is_valid():
            username = request.POST['username']
            password = request.POST['password1']
            fullname = request.POST['fullname']
            phone = request.POST['phone']
            card = request.POST['card']
            address = request.POST['address']
            sql = "INSERT INTO bookstore_customer VALUES\
            ('password',NULL,'0','%s','%s','%s','%s','%s','1','1');"%(username,fullname,phone,card,address)
            cur.execute(sql) 
            u = Customer.objects.get(username=username)
            u.set_password("%s"% password)
            u.save()
            registered = True
        else:
            print user_form.errors
    else:
        user_form = CustomerCreationForm()
    return render_to_response('bookstore/signup.html',{'user_form': user_form, 'registered': registered,'base_template':'base.html'},context)

@login_required(login_url='/login')
def logoutView(request, onsuccess='/login', onfail='/bookstore'):
    if request.user.is_authenticated():
        logout(request)
        return redirect(onsuccess)
    else:
        return redirect(onfail)

@login_required(login_url='/login')
def order(request):
    context = RequestContext(request)
    cur = connection.cursor()
    completed = False
    book_list = ""
    ISBN = ""
    if request.method == 'POST':
        ISBN = request.POST['order_isbn']
        copies = request.POST['spinner']
        if not copies.isdigit():
            return HttpResponseRedirect('/bookstore/order')
        else:
            copies = int(copies)
        if copies==0:
            return HttpResponseRedirect('/bookstore/order')
        else:
            cur.execute("SELECT copies FROM bookstore_book WHERE ISBN = '%s'"%(ISBN))
            avail = int(cur.fetchone()[0])  
            if avail>=copies:
                username = request.user.username
                now=datetime.datetime.now()
                date="%s/%s/%s" % (now.day, now.month, now.year)
                cur.execute("INSERT INTO bookstore_order (customer_id,book_id,order_date,order_status,copies) \
                    VALUES ('%s','%s','%s','completed','%s')"%(username,ISBN,date,copies))
                cur.execute("UPDATE bookstore_book SET copies='%d' WHERE ISBN='%s'"%(avail-copies,ISBN))
                completed = True
            else:
                return HttpResponseRedirect('/bookstore/order')
    if completed:
        username = request.user.username
        sql = "SELECT title,author,ISBN from bookstore_book where ISBN in (SELECT book_id FROM \
            (SELECT book_id, count(*) as num from bookstore_order where customer_id in \
            (SELECT customer_id from bookstore_order where book_id = '%s' and customer_id != '%s')\
            and book_id != '%s'\
            group by book_id order by num desc) T) "%(ISBN,username,ISBN)
        cur.execute(sql)
        columns = [col[0] for col in cur.description]
        book_list = [dict(zip(columns, row)) for row in cur.fetchall()][:3]       
    return render(request,'bookstore/finish.html',{'completed':completed,'book_list':book_list,'ISBN':ISBN,'base_template':'base_auth.html'})

@login_required(login_url='/login')
def orderRecords(request):
    cur = connection.cursor()
    username = request.user.username
    try:
        cur.execute("SELECT id,book_id,title,order_date,order_status,bookstore_order.copies FROM \
            bookstore_order JOIN bookstore_book WHERE bookstore_order.book_id=bookstore_book.ISBN \
            AND customer_id='%s' AND order_status='completed' order by id desc"%(username))
        columns = [col[0] for col in cur.description]
        order_list = [dict(zip(columns, row)) for row in cur.fetchall()]
    except:
        order_list = null
    paginator = Paginator(order_list, 20)
    page = request.GET.get('page')
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        orders = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        orders = paginator.page(paginator.num_pages)
    return render(request,'bookstore/order_record.html',{'order_list': order_list,'orders':orders,'base_template':'base_auth.html'})

@login_required(login_url='/login')
def account(request,count=3):
    isManager = request.user.is_superuser
    if(isManager):
        return manager_account(request,count)
    else:
        return customer_account(request)

def customer_account(request):
    context = RequestContext(request)
    cur = connection.cursor()
    username = request.user.username
    isManager = request.user.is_superuser
    edited = False
    try:
        cur.execute("SELECT username,fullname,phone,card,address \
            FROM bookstore_customer WHERE username='%s'"%(username))
        columns = [col[0] for col in cur.description]
        user_info = [dict(zip(columns, row)) for row in cur.fetchall()]
        cur.execute("SELECT title,text,score,date FROM bookstore_feedback,bookstore_book\
            WHERE customer_id='%s' AND bookstore_feedback.book_id=bookstore_book.ISBN"%(username))
        columns = [col[0] for col in cur.description]
        feedback_list = [dict(zip(columns, row)) for row in cur.fetchall()]
        sql= "SELECT f.customer_id,f.text,b.title,r.rate FROM bookstore_rating r,bookstore_feedback f,bookstore_book b\
                    WHERE r.customer_id = '%s' AND r.rater_id=f.customer_id AND r.book_id=f.book_id \
                    AND r.book_id=b.ISBN;"%(username)
        cur.execute(sql)
        columns = [col[0] for col in cur.description]
        rate_list = [dict(zip(columns, row)) for row in cur.fetchall()]
    except:
        user_info = ""
        feedback_list = ""
        rate_list = ""
    if request.method == 'POST':
        user_form = CustomerChangeForm(data=request.POST)
        if user_form.is_valid():
            fullname = request.POST['fullname']
            phone = request.POST['phone']
            card = request.POST['card']
            address = request.POST['address']
            sql = "UPDATE bookstore_customer SET \
            fullname='%s', phone='%s', card='%s',address='%s';"%(fullname,phone,card,address)
            cur.execute(sql) 
            edited = True
            return HttpResponseRedirect('/bookstore/account')
        else:
            print user_form.errors
    else:
        user_form = CustomerChangeForm()
    return render_to_response('bookstore/account_info.html',{'feedback_list':feedback_list,'user_info':user_info,
        'user_form': user_form, 'rate_list':rate_list,'edited': edited,'base_template':'base_auth.html',
        'isManager':isManager},context)

def manager_account(request,count):
    context = RequestContext(request)
    cur = connection.cursor()
    isManager = request.user.is_superuser
    book_list=""
    count = int(count)
    try:
        now=datetime.datetime.now()
        date="%"+ "%s/%s" % (now.month, now.year) 
        sql = "SELECT ISBN,title,author FROM bookstore_book WHERE ISBN IN (SELECT book_id FROM (SELECT book_id, count(*) AS num \
            FROM bookstore_order WHERE order_date LIKE '%s'  GROUP BY book_id ORDER BY num DESC) T);"%(date)       
        cur.execute(sql)
        columns = [col[0] for col in cur.description]
        pop_book = [dict(zip(columns, row)) for row in cur.fetchall()][:count]
        sql2 = "SELECT b1.author, count(*) AS num FROM bookstore_book b1, bookstore_order o1 WHERE b1.ISBN = o1.book_id\
                AND order_date LIKE '%s'GROUP BY b1.author ORDER BY num DESC;"%(date)   
        cur.execute(sql2)        
        columns = [col[0] for col in cur.description]
        pop_author = [dict(zip(columns, row)) for row in cur.fetchall()][:count]
        sql3 = "SELECT b1.publisher, count(*) AS num FROM bookstore_book b1, bookstore_order o1 WHERE b1.ISBN = o1.book_id\
                AND order_date LIKE '%s' GROUP BY b1.publisher ORDER BY num DESC;"%(date)
        cur.execute(sql3)      
        columns = [col[0] for col in cur.description]
        pop_publisher = [dict(zip(columns, row)) for row in cur.fetchall()][:count]
    except:
        return HttpResponse("error")
    return render_to_response('bookstore/account_info.html',{'count':count,'pop_book':pop_book, 'pop_publisher':pop_publisher,'pop_author':pop_author,
        'base_template':'base_auth.html','isManager':isManager},context)

@login_required(login_url='/login')
def add(request):
    context = RequestContext(request)
    cur = connection.cursor()
    completed = False
    if request.method == 'POST':
        ISBN = request.POST['add_isbn']
        copies = request.POST['add_copies']
        title = request.POST['add_title']
        try:
            copies = int(copies)
        except:
            return HttpResponseRedirect('/bookstore/order')
        cur.execute("SELECT copies FROM bookstore_book WHERE ISBN = '%s'"%(ISBN))
        avail = int(cur.fetchone()[0])  
        if copies+avail<0:
            return HttpResponseRedirect('/bookstore/order')
        else:
            cur.execute("UPDATE bookstore_book SET copies='%d' WHERE ISBN='%s'"%(avail+copies,ISBN))
            completed = True
    return render(request,'bookstore/finish_add_book.html',{'completed':completed,'title':title,'copies':copies,
        'ISBN':ISBN,'base_template':'base_auth.html'})

@login_required(login_url='/login')
def addNewBook(request):
    context = RequestContext(request)
    cur = connection.cursor()
    created = False
    if request.method == 'POST':
        book_form = BookCreationForm(data=request.POST)
        if book_form.is_valid():
            ISBN = request.POST['ISBN']
            title = request.POST['title']
            author = request.POST['author']
            publisher = request.POST['publisher']
            keywords = request.POST['keywords']
            subject = request.POST['subject']
            format = request.POST['format']
            year = request.POST['year_of_publication']
            price = request.POST['price']
            copies = request.POST['copies']
            sql = "INSERT INTO bookstore_book VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');"\
            %(ISBN,title,publisher,author,keywords,subject,format,year,price,copies)
            cur.execute(sql) 
            created = True
        else:
            print book_form.errors
    else:
        book_form = BookCreationForm()
    return render_to_response('bookstore/add_book.html',{'book_form': book_form,'created':created,'base_template':'base_auth.html'},context)



@login_required(login_url='/login')
def vote(request,isbn):
    cur = connection.cursor()
    if request.method == 'POST':
        score = request.POST['vote_score']
        rater = request.POST['vote_rater']
        username = request.user.username
        if username != rater:
            try:
                sql = "INSERT INTO bookstore_rating VALUES ('%s','%s','%s','%s')"%(username, rater, isbn, score)
                cur.execute(sql)
                # return redirect("/bookstore/detail/%s"%isbn)
                return redirect(reverse("detail",args=[isbn,0,3]))
            except:
                return redirect(reverse("detail",args=[isbn,0,2]))
        else:
            return redirect(reverse("detail",args=[isbn,0,1]))


    










