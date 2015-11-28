from django.shortcuts import render,render_to_response, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.core.context_processors import csrf
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Book,Customer
from .forms import CustomerCreationForm
from django.db import connection

@login_required(login_url='/login')
def index(request):
    book_list = ""
    try:
        cur = connection.cursor()
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
            sql = "insert into bookstore_customer values('password',null,'0','%s','%s','%s','%s','%s','1','1');"%(username,fullname,phone,card,address)
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
