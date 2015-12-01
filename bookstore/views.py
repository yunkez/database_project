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
        cur.execute("SELECT * FROM bookstore_book;")
        columns = [col[0] for col in cur.description]
        book_list = [dict(zip(columns, row)) for row in cur.fetchall()]
    except:
        book_list = ""
    if request.method == 'POST':
        author = request.POST['search_author'] 
        publisher = request.POST['search_publisher'] 
        title = request.POST['search_title'] 
        subject = request.POST['search_subject']
        orderby = int(request.POST['orderby'])
        page_title = "Your Search Results "
        if orderby==1:
            sql = "SELECT * from bookstore_book where title LIKE '%s' and author LIKE '%s' and publisher \
            LIKE '%s' and subject LIKE '%s' order by year_of_publication;" %\
            (searchValue(title),searchValue(author),searchValue(publisher),searchValue(subject))
    
        else:
            sql ="SELECT b1.* from bookstore_book b1 join bookstore_feedback where b1.title LIKE '%s' \
            and b1.author LIKE '%s' and b1.publisher LIKE'%s' and b1.subject LIKE '%s' \
            group by b1.ISBN order by AVG(score);"%\
            (searchValue(title),searchValue(author),searchValue(publisher),searchValue(subject))
        cur.execute(sql)
        columns = [col[0] for col in cur.description]
        book_list = [dict(zip(columns, row)) for row in cur.fetchall()]
    return render(request, 'bookstore/index.html',{'book_list': book_list,'author':author,'subject':subject,
            'title':title,'publisher':publisher,'orderby':orderby,'base_template':'base_auth.html',
            'page_title':page_title,'isManager':isManager})

def searchValue(s):
    return "%"+s+"%"

@login_required(login_url='/login')
def detail(request,isbn):
    cur = connection.cursor()
    isManager = request.user.is_superuser
    try:
        # sql = "SELECT f1.* FROM bookstore_feedback f1 JOIN (SELECT r1.customer_id, r1.book_id, AVG(r1.rate) \
        #     AS average FROM bookstore_rating r1 GROUP BY r1.book_id, r1.customer_id HAVING book_id = '%s') AS temp \
        #     ORDER BY temp.average DESC;"%(isbn)
        cur.execute("SELECT * FROM bookstore_feedback WHERE book_id='%s';"%(isbn))
        columns = [col[0] for col in cur.description]
        feedback_list = [dict(zip(columns, row)) for row in cur.fetchall()]
        cur.execute("SELECT * FROM bookstore_book WHERE ISBN='%s';"%(isbn))
        columns = [col[0] for col in cur.description]
        book = [dict(zip(columns, row)) for row in cur.fetchall()]
    except:
        book = ""
        feedback_list = "" 
    return render(request, 'bookstore/index_detail.html',{'feedback_list':feedback_list,'book': book[0],
        'isManager':isManager,'base_template':'base_auth.html'})

@login_required(login_url='/login')
def feedback(request):
    cur = connection.cursor()
    text = request.POST['feedback_text']
    ISBN = request.POST['feedback_isbn']
    score = request.POST['feedback_score']
    username = request.user.username
    now=datetime.datetime.now()
    date="%s/%s/%s" % (now.day, now.month, now.year)
    try:
        sql = "INSERT INTO bookstore_feedback VALUES ('%s','%s','%s','%s','%s')"%\
                (ISBN,username, text,score,date)
        cur.execute(sql)
    except:
        return HttpResponse("Invalid request")
    return HttpResponseRedirect('/bookstore/detail/'+ISBN)

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
    if request.method == 'POST':
        ISBN = request.POST['order_isbn']
        copies = int(request.POST['spinner'])  
        try:
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
                info = "Not enough stock"
        except Book.DoesNotExist:
            info = "Please enter a valid ISBN."
    if completed:
        username = request.user.username
        sql = "SELECT title,author from bookstore_book where ISBN in (SELECT book_id FROM \
            (SELECT book_id, count(*) as num from bookstore_order where customer_id in \
            (SELECT customer_id from bookstore_order where book_id = '%s' and customer_id != '%s')\
            and book_id != '%s'\
            group by book_id order by num desc) T) "%(ISBN,username,ISBN)
        cur.execute(sql)
        columns = [col[0] for col in cur.description]
        book_list = [dict(zip(columns, row)) for row in cur.fetchall()]       
    return render(request,'bookstore/finish.html',{'completed':completed,'book_list':book_list,'base_template':'base_auth.html'})

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
    return render(request,'bookstore/order_record.html',{'order_list': order_list,'base_template':'base_auth.html'})

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
        cur.execute("SELECT title, text,score,date FROM bookstore_feedback,bookstore_book\
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
        sql = "SELECT ISBN,title FROM bookstore_book WHERE ISBN IN (SELECT book_id FROM (SELECT book_id, count(*) AS num \
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
        copies = int(request.POST['add_copies']) 
        title = request.POST['add_title']
        try:
            cur.execute("SELECT copies FROM bookstore_book WHERE ISBN = '%s'"%(ISBN))
            avail = int(cur.fetchone()[0])  
            cur.execute("UPDATE bookstore_book SET copies='%d' WHERE ISBN='%s'"%(avail+copies,ISBN))
            completed = True
        except Book.DoesNotExist:
            info = "Please enter a valid ISBN."
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
                return HttpResponseRedirect("/bookstore/detail/%s"%isbn)
            except:
                return HttpResponse("You cannot vote twice!")
        else:
            return HttpResponse("You cannot vote for yourself!")
    










