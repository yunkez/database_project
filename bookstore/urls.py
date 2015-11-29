from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^logout/$', views.logoutView, name='logout'),
    url(r'^order/$', views.order, name='order'),
    url(r'^shoppingcart/$', views.shoppingcart, name='shoppingcart'),
    url(r'^myorderrecords/$', views.orderRecords, name='orderRecords')

]