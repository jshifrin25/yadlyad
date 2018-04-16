from django.urls import include, path
from django.contrib.staticfiles.views import serve
from django.contrib.auth import views as auth_views
from yadlyad.admin import admin_site
from . import views

urlpatterns = [
    # Examples:
    path('', views.home, name='home'),
    # url(r'^blog/', include('blog.urls')),
    path('static/<path>.*)/', serve),
    path('orders/', include('order.urls')),
    # url(r'^deliveries/', include('order_delivery.urls', namespace="deliveries")),
    path('accounts/login/', auth_views.login, {'template_name': 'yadlyad/login.html'},  name="login"),
    path('logout/', auth_views.logout_then_login, {'login_url': '/orders/','current_app': 'orders:order'}, name="logout"),
    path('admin/', admin_site.urls)
]
