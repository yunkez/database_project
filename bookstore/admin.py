from django.contrib import admin
from .models import Book, Customer, Feedback, Order, Rating

admin.site.register(Book)
admin.site.register(Customer)
admin.site.register(Feedback)
admin.site.register(Order)
admin.site.register(Rating)

