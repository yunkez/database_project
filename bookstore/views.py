from django.shortcuts import render,render_to_response, redirect
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.core.context_processors import csrf
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Book,Customer
from .serializers import BookSerializer

@login_required(login_url='/login/')
def index(request):
	book_list = Book.objects.order_by('title')
	context = {'book_list': book_list, 'user': request.user,}
	return render(request, 'bookstore/index.html', context)

def book_list(request):
    if request.method == 'GET':
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = BookSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

def loginview(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('bookstore/login.html', c)

def auth_and_login(request, onsuccess='/bookstore', onfail='/login'):
    user = authenticate(username=request.POST['email'], password=request.POST['password'])
    if user is not None:
        login(request, user)
        return redirect(onsuccess)
    else:
        return redirect(onfail) 

def sign_up_in(request):
    post = request.POST
    if not user_exists(post['email']): 
        user = create_user(username=post['email'], email=post['email'], password=post['password'])
        return auth_and_login(request)
    else:
        return redirect("/bookstore/login")

def create_user(username, email, password):
    user = User(username=username, email=email)
    user.set_password(password)
    user.save()
    return user
 
def user_exists(username):
    user_count = User.objects.filter(username=username).count()
    if user_count == 0:
        return False
    return True

def logoutView(request, onsuccess='/login', onfail='/bookstore'):
    if request.user.is_authenticated():
        logout(request)
        return redirect(onsuccess)
    else:
        return redirect(onfail)

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)
