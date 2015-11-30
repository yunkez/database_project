from django.shortcuts import render,render_to_response, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.core.context_processors import csrf
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Book,Customer
from .forms import CustomerCreationForm,CustomerChangeForm
from django.db import connection
import datetime
import ast

@login_required(login_url='/login')
def index(request):
    book_list = ""
    cur = connection.cursor()
    try:
        cur.execute("select * from bookstore_book")
        columns = [col[0] for col in cur.description]
        book_list = [dict(zip(columns, row)) for row in cur.fetchall()]
    except:
        book_list = "" 
    return render(request, 'bookstore/index.html',{'book_list': book_list,'base_template':'base_auth.html'})

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
            sql = "INSERT INTO bookstore_customer VALUES('password',NULL,'0','%s','%s','%s','%s','%s','1','1');"%(username,fullname,phone,card,address)
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

def logoutView(request, onsuccess='/login', onfail='/bookstore'):
    if request.user.is_authenticated():
        logout(request)
        return redirect(onsuccess)
    else:
        return redirect(onfail)

def order(request):
    context = RequestContext(request)
    cur = connection.cursor()
    completed = False
    if request.method == 'POST':
        ISBN = request.POST['order_isbn']
        copies = int(request.POST['order_copies'])  
        try:
            cur.execute("SELECT copies FROM bookstore_book WHERE ISBN = '%s'"%(ISBN))
            avail = int(cur.fetchone()[0])  
            if avail>=copies:
                username = request.user.username
                now=datetime.datetime.now()
                date="%s/%s/%s" % (now.day, now.month, now.year)
                cur.execute("INSERT INTO bookstore_order (customer_id,book_id,order_date,order_status,copies) VALUES ('%s','%s','%s','completed','%s')"%(username,ISBN,date,copies))
                cur.execute("UPDATE bookstore_book SET copies='%d' WHERE ISBN='%s'"%(avail-copies,ISBN))
                completed = True
            else:
                info = "Not enough stock"
        except Book.DoesNotExist:
            info = "Please enter a valid ISBN."
    if completed:
        username = request.user.username
        sql = "SELECT book_id, count(*) as num from bookstore_order where customer_id in \
            (SELECT customer_id from bookstore_order where book_id = '%s' and customer_id != '%s')\
            and book_id != '%s'\
            group by book_id order by num desc"%(ISBN,username,ISBN)
        cur.execute(sql)
        columns = [col[0] for col in cur.description]
        book_list = [dict(zip(columns, row)) for row in cur.fetchall()]
        return render(request,'bookstore/finish.html',{'book_list':book_list,'base_template':'base_auth.html'})
    else:
        return HttpResponse("Your request is invalid.")

def orderRecords(request):
    cur = connection.cursor()
    username = request.user.username
    try:
        cur.execute("SELECT id,book_id,order_date,order_status FROM bookstore_order WHERE customer_id='%s' AND order_status='submitted'"%(username))
        columns = [col[0] for col in cur.description]
        order_list = [dict(zip(columns, row)) for row in cur.fetchall()]
    except:
        order_list = null
    return render(request,'bookstore/order_record.html',{'order_list': order_list,'base_template':'base_auth.html'})

def account(request):
    context = RequestContext(request)
    cur = connection.cursor()
    username = request.user.username
    edited = False
    try:
        cur.execute("SELECT username,fullname,phone,card,address FROM bookstore_customer WHERE username='%s'"%(username))
        columns = [col[0] for col in cur.description]
        user_info = [dict(zip(columns, row)) for row in cur.fetchall()]
    except:
        user_info = null
    if request.method == 'POST':
        user_form = CustomerChangeForm(data=request.POST)
        if user_form.is_valid():
            fullname = request.POST['fullname']
            phone = request.POST['phone']
            card = request.POST['card']
            address = request.POST['address']
            sql = "UPDATE bookstore_customer SET fullname='%s', phone='%s', card='%s',address='%s';"%(fullname,phone,card,address)
            cur.execute(sql) 
            edited = True
            return HttpResponseRedirect('/bookstore/account')
        else:
            print user_form.errors
    else:
        user_form = CustomerChangeForm()
    return render_to_response('bookstore/account_info.html',{'user_info':user_info,'user_form': user_form, 'edited': edited,'base_template':'base.html'},context)

# def finish(request):
#     cur = connection.cursor()
#     username = request.user.username
#     sql = "SELECT book_id, count(*) as num from bookstore_order where customer_id in \
#         (SELECT customer_id from bookstore_order where book_id = '%s' and customer_id != '%s')\
#         and book_id != '%s'\
#         group by book_id order by num desc"%('9780470624708',username,'9780470624708')
#     cur.execute(sql)
#     columns = [col[0] for col in cur.description]
#     book_list = [dict(zip(columns, row)) for row in cur.fetchall()]
#     return render(request,'bookstore/finish.html',{'book_list':book_list,'base_template':'base_auth.html'})



