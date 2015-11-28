from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin

### model class for books
class Book(models.Model):
    ISBN = models.BigIntegerField(primary_key=True)
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

class CustomerManager(BaseUserManager):
    def create_user(self,username,password,fullname,phone,card,address):
        user = self.model(
            username = username,
            fullname = fullname,
            phone = phone,
            card= card,
            address = address,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,username,password,fullname,phone,card,address):
        user = self.model(
            username = username,
            fullname = fullname,
            phone = phone,
            card= card,
            address = address,
        )
        user.is_staff = True
        user.is_superuser = True 
        user.set_password(password)
        user.save(using=self._db)
        return user

class Customer(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True,primary_key=True)
    fullname = models.CharField(max_length=100)
    phone = models.BigIntegerField()
    card = models.BigIntegerField()
    address = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['fullname','phone','card','address']
    objects = CustomerManager()

    def __unicode__(self):
        return self.fullname

    def get_full_name(self):
        return self.fullname

    def get_short_name(self):
        return self.fullname


class Opinion(models.Model):
    customer = models.ForeignKey(Customer)
    book = models.ForeignKey(Book)
    text = models.TextField()
    score = models.IntegerField(
        choices=((1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5'),(6, '6'),(7, '7'),(8, '8'),(9, '9'),(10, '10')
    ))

    def __unicode__(self):
        return self.customer.full_name + " : " + self.book.title
