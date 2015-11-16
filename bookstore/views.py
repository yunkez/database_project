from django.shortcuts import render
from django.http import HttpResponse
from .models import Book

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def index(request):
    book_list = Book.objects.order_by('title')
#    output = ', '.join([b.title for b in book_list])
#    return HttpResponse(output)

    context = {'book_list': book_list}
    return render(request, 'bookstore/login.html', context)