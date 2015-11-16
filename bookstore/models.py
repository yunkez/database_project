from django.db import models


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

class Customer(models.Model):
	full_name = models.CharField(max_length=100)
	login_name = models.CharField(max_length=100)
	password = models.CharField(max_length=100)
	card_number = models.BigIntegerField()
	address = models.CharField(max_length=100)
	card_number = models.BigIntegerField()
	def __unicode__(self):
		return self.full_name

class Opinion(models.Model):
    customer = models.ForeignKey(Customer)
    book = models.ForeignKey(Book)
    text = models.TextField()
    score = models.IntegerField(
        choices=((1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5'),(6, '6'),(7, '7'),(8, '8'),(9, '9'),(10, '10'),
       	))

    def __unicode__(self):
        return self.customer.full_name + " : " + self.book.title




	