from django.conf.urls import patterns, url
from order import views

urlpatterns = [
    url(r'^order-history/$', views.IndexView.as_view(), name='index'),
    url(r'^$', views.order, name='order'),
    url(r'^order/(?P<pk>\d+)/$', views.OrderDetailView.as_view(),
        name='order-detail'),
]
