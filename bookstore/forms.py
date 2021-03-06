from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from .models import Customer,Book
from django import forms

class CustomerCreationForm(forms.ModelForm):
	password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'password'}))
	password2 = forms.CharField(label="Confirm your password",widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'confirm your password'}))

	class Meta:
		model = Customer
		fields = ['username','fullname','phone','card','address']
		widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'login name','required': True}),
            'fullname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'full name','required': True}),
            'phone': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'phone number','required': True}),
            'card': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'card number','required': True}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'address','required': True}),
        }

	def clean_password2(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1!=password2:
			raise forms.ValidationError("Password does not match.")
		return password2

	def save(self, commit=True):
	    user = super(CustomerCreationForm, self).save(commit=False)
	    user.set_password(self.cleaned_data["password1"])
	    if commit:
	        user.save()
	    return user

class CustomerChangeForm(forms.ModelForm): 

    class Meta:
        model = Customer
        fields = ['fullname','phone','card','address']
        widgets = {
            'fullname': forms.TextInput(attrs={'class': 'form-control','id':'user_fullname', 'placeholder': 'edit full name here'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control','id':'user_phone', 'placeholder': 'edit phone number here'}),
            'card': forms.NumberInput(attrs={'class': 'form-control','id':'user_card', 'placeholder': 'edit card number here'}),
            'address': forms.TextInput(attrs={'class': 'form-control','id':'user_address', 'placeholder': 'edit address here'}),
        }

	def clean_password(self):
		return ""


class BookCreationForm(forms.ModelForm):
	class Meta:
		model = Book
		fields = '__all__'
		# widgets = {
  #           'ISBN': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ISBN','required': True}),
  #           'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'book title','required': True}),
  #           'publisher': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'publisher name','required': True}),
  #           'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'author name','required': True}),
  #           'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'subject','required': True}),
  #           'keywords': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'keywords','required': True}),
  #           'format': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'format','required': True}),
  #           'year_of_publication': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'publication year','required': True}),
  #           'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'book price','required': True}),
  #           'copies': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'number of copies','required': True}),
  #       }
