from django.contrib import admin
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import Book, Customer, Opinion

admin.site.register(Book)
admin.site.register(Opinion)

class CustomerCreationForm(forms.ModelForm):
	password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
	password2 = forms.CharField(label="Confirm your password",widget=forms.PasswordInput)

	class Meta:
		model = Customer
		fields = ['login_name','full_name','phone_number','card_number','address']

	def clean_password2(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1!=password2:
			raise forms.ValidationError("Password does not match.")
		return password2

	def save(self, commit=True):
	    user = super(CustomerCreationForm  , self).save(commit=False)
	    user.set_password(self.cleaned_data["password1"])
	    if commit:
	        user.save()
	    return user

class CustomerChangeForm(forms.ModelForm): 
    password = ReadOnlyPasswordHashField(label="Password")

    class Meta:
        model = Customer
        fields = '__all__'

    def clean_password(self):
        return self.initial["password"]

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
