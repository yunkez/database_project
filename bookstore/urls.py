from django.conf.urls import url
from . import views
urlpatterns = [
	url(r'^$', views.book_list, name = "book_list"),
]