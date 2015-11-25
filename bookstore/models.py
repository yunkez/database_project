from django.db import models

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

