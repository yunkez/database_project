from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'ISBN', 'title', 'publisher', 'author', 'keywords',
        		'subject','format','year_of_publication','price','copies')
