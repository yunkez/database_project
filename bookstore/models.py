from django.db import models

class Book(models.Model):
	ISBN = models.BigIntegerField()
	title = models.CharField(max_length=100)
	publisher = models.CharField(max_length=100)
	author = models.CharField(max_length=100)
	keywords = models.CharField(max_length=100)
	subject = models.CharField(max_length=100)
	format = models.CharField(max_length=9,
        choices = (
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
	login_name = models.CharField(max_length=100, unique=True)
	full_name = models.CharField(max_length=100)
	phone_number = models.BigIntegerField()
	card_number = models.BigIntegerField()
	address = models.CharField(max_length=100)
	password = models.CharField(max_length=100)
	def __unicode__(self):
		return self.full_name

class Feedback(models.Model):
	score = models.PositiveIntegerField()
	text = models.CharField(max_length = 300)
	book = models.ForeignKey(Book)
	customer = models.ForeignKey(Customer)
	def __unicode__(self):
		return u'%s reviews %s' %(self.customer.full_name, self.book.title)

class Order(models.Model):
	order_date = models.DateField(auto_now_add = True)
	order_status = models.CharField(max_length=9,
		choices = (('submitted', 'submitted'),('executed', 'executed'),))
	book = models.ForeignKey(Book)
	customer = models.ForeignKey(Customer)
	def __unicode__(self):
		return u'%s orders %s on %s' %(self.customer.full_name, self.book.title, self.order_date)

class Rating(models.Model):
	rater = models.ForeignKey(Customer)
	feedback = models.ForeignKey(Feedback)
	rate = models.PositiveIntegerField()
	def __unicode__(self):
		return u'%s rates %s for feedback of %s on %s' %(self.rater.full_name, self.feedback.customer.full_name, self.feedback.book.title)

		


		


