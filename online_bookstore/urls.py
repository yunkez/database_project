from django.conf.urls import include, url
from django.contrib import admin
from bookstore import views

urlpatterns = [
	url(r'^bookstore/', include('bookstore.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
]
