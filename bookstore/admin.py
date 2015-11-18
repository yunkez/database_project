from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import Book, Customer, Opinion
from .forms import CustomerCreationForm, CustomerChangeForm
admin.site.register(Book)
admin.site.register(Opinion)


class CustomerAdminForm(UserAdmin):
	form = CustomerChangeForm
	add_form = CustomerCreationForm

	list_display  = ['login_name','full_name','phone_number','card_number','address']
	list_filter = ['login_name']
	ordering = ['login_name']

	fieldsets = (
		(None, {'fields': ('login_name', 'password')}),
		('Personal Info',{'fields': ('full_name','phone_number','card_number','address')})
	)

	add_fieldsets = (
		(None, {'fields': ('login_name', 'full_name','password1','password2')})
	)


admin.site.unregister(Group)
admin.site.register(Customer,CustomerAdminForm)
