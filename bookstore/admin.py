from django.contrib import admin

# Register your models here.
from .models import Book, Customer, Opinion

admin.site.register(Book)
admin.site.register(Customer)
admin.site.register(Opinion)