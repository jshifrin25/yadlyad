from django.conf.urls import url
from order import views

urlpatterns = [
    url(r'^order-history/$', views.IndexView.as_view(), name='index'),
    url(r'^$', views.order, name='order'),
    url(r'^(?P<order_id>\d+)$',  views.order,  name = 'order'), 
    url(r'^reset/$', views.reset_order, name='reset'), 
    url(r'^order/(?P<pk>\d+)/$', views.OrderDetailView.as_view(),name='order-detail'),
]
