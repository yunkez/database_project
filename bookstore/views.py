from django.shortcuts import render
from django.http import HttpResponse
from .models import Book,Customer

def index(request):
	book_list = Book.objects.order_by('title')
	current_user = Customer.objects.order_by("full_name")[0]
	context = {'book_list': book_list, 'username': current_user.full_name,}
	return render(request, 'bookstore/index.html', context)