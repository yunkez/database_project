from django.db import models
from django import forms
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin

### model class for books
class Book(models.Model):
	ISBN = models.BigIntegerField()
	title = models.CharField(max_length=100)
	publisher = models.CharField(max_length=100)
	author = models.CharField(max_length=100)
	keywords = models.CharField(max_length=100)
	subject = models.CharField(max_length=100)
	format = models.CharField(max_length=9,
	        choices=(
	            ('hardcover', 'hardcover'),
	            ('softcover', 'softcover'),
	        )
	    )
	year_of_publication = models.PositiveIntegerField()
	price = models.PositiveIntegerField()
	copies = models.PositiveIntegerField()
	def __unicode__(self):
		return self.title

class CustomerAdmin(BaseUserManager):
	def create_user(self,login_name,password,full_name,phone_number,card_number,address):
		user = self.model(
			login_name = login_name,
			full_name = full_name,
			phone_number = phone_number,
			card_number = card_number,
			address = address,
		)
		user.set_password(password)
		user.save()
		return user

	def create_superuser(self,login_name,password,full_name,phone_number,card_number,address):
		user = self.model(
			login_name = login_name,
			full_name = full_name,
			phone_number = phone_number,
			card_number = card_number,
			address = address,
		)
		user.is_superuser = True 
		user.set_password(password)
		user.save()
		return user

class Customer(AbstractBaseUser, PermissionsMixin):
	login_name = models.CharField(max_length=100, unique=True)
	full_name = models.CharField(max_length=100)
	phone_number = models.BigIntegerField()
	card_number = models.BigIntegerField()
	address = models.CharField(max_length=100)
	is_staff = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)

	USERNAME_FIELD = 'login_name'
	REQUIRED_FIELDS = ['full_name','phone_number','card_number','address']
	objects = CustomerAdmin()

	def __unicode__(self):
	    return self.full_name

	def get_full_name(self):
		return self.full_name

	def get_short_name(self):
		return self.full_name



class Opinion(models.Model):
    customer = models.ForeignKey(Customer)
    book = models.ForeignKey(Book)
    text = models.TextField()
    score = models.IntegerField(
        choices=((1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5'),(6, '6'),(7, '7'),(8, '8'),(9, '9'),(10, '10')
    ))

    def __unicode__(self):
        return self.customer.full_name + " : " + self.book.title


		



	