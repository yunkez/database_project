from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'([0-9]{13})/$', views.detail, name='detail'),
    url(r'^logout/$', views.logoutView, name='logout'),
    url(r'^order/$', views.order, name='order'),
    url(r'^add/$', views.add, name='add'),
    url(r'^addnewbook/$', views.addNewBook, name='addNewBook'),
    url(r'^feedback/$', views.feedback, name='feedback'),
    url(r'^myorderrecords/$', views.orderRecords, name='orderRecords'),
    url(r'^account/$', views.account, name='account'),
    url(r'^account/([0-9])/$', views.account, name='account'),
    # url(r'^success/$', views.finish, name='finish')


]