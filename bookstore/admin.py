from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import Book, Customer,Feedback,Order,Rating
from .forms import CustomerCreationForm, CustomerChangeForm


admin.site.register(Book)
admin.site.register(Feedback)
admin.site.register(Order)
admin.site.register(Rating)

# Register your models here.


class CustomerAdminForm(UserAdmin):
	form = CustomerChangeForm
	add_form = CustomerCreationForm

	list_display  = ['username','fullname','phone','card','address']
	list_filter = ['username']
	ordering = ['fullname']
	fieldsets = (
		(None, {'fields': ('username', 'password')}),
		('Personal Info',{'fields': ('fullname','phone','card','address')}))
	add_fieldsets = (
		(None,{'fields:':('username','fullname','password1','password2')}))
	filter_horizontal = ()

admin.site.unregister(Group)
admin.site.register(Customer,CustomerAdminForm)
