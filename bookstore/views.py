from django.shortcuts import render,render_to_response, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.core.context_processors import csrf
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Book,Customer
from .serializers import BookSerializer
from .forms import CustomerCreationForm

@login_required(login_url='/login')
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
        return render_to_response('bookstore/login.html', {}, context)

def register(request):
    context = RequestContext(request)
    registered = False
    if request.method == 'POST':
        user_form = CustomerCreationForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            registered = True
        else:
            print user_form.errors
    else:
        user_form = CustomerCreationForm()
    return render_to_response('bookstore/signup.html',{'user_form': user_form, 'registered': registered},context)

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
