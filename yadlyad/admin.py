from django.contrib.admin import AdminSite
from django.contrib.auth.models import User,Group
from order.models import Order, Product, Category
from order.admin import OrderAdmin, ProductAdmin, CategoryAdmin
from order_delivery.admin import DeliveryAdmin
from order_delivery.models import Delivery

class YadlYadAdminSite(AdminSite):
    site_header = "Yad l' Yad Adminstration"
    site_url = '/orders/'
    site_title = 'Yad L Yad Order Site'
    
admin_site = YadlYadAdminSite(name="ylyadmin")
admin_site.register(Group)
admin_site.register(User)
admin_site.register(Order, OrderAdmin)
admin_site.register(Product, ProductAdmin)
admin_site.register(Category, CategoryAdmin)
admin_site.register(Delivery, DeliveryAdmin)