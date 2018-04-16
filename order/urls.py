from django.urls import path
from order import views

urlpatterns = [
    path('order-history/', views.IndexView.as_view(), name='index'),
    path('', views.order, name='order'),
    path('<int:order_id>',  views.order,  name = 'order'), 
    path('reset/', views.reset_order, name='reset'), 
    path('<int:pk>/', views.OrderDetailView.as_view(),name='order-detail'),
]
