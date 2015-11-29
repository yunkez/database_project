from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^logout/$', views.logoutView, name='logout'),
    # url(r'^order/(?P<ISBN>[0-9]{13})/$', views.order, name='order'),
    url(r'^order/$', views.order, name='order')
]