from django.shortcuts import render
from django.http import HttpResponse
from .models import Book,Customer
from .serializers import BookSerializer

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser


def index(request):
	book_list = Book.objects.order_by('title')
	current_user = Customer.objects.order_by("full_name")[0]
	context = {'book_list': book_list, 'username': current_user.full_name,}
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


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)
