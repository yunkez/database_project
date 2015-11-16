from django.db import models


### model class for books
class Book(models.Model):
	ISBN = models.BigIntegerField()
    title = models.CharField(max_length=100)
	publisher = models.CharField(max_length=100)
	author = models.CharField(max_length=100)
	keywords = models.CharField(max_length=100)
	subject = models.CharField(max_length=100)
	format = models.CharField(max_length=100)
	year_of_publication = models.PositiveIntegerField()
	price = models.PositiveIntegerField()
	copies = models.PositiveIntegerField()
	#    year_of_publication = models.PositiveIntegerField(null=True,
	#        validators=[util.not_negative])

    def __unicode__(self):
        return self.title

class Book(models.Model):
	ISBN = models.BigIntegerField()
    title = models.CharField(max_length=100)
	publisher = models.CharField(max_length=100)
	author = models.CharField(max_length=100)