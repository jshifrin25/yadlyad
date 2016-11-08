from django.conf.urls import include, url
from django.contrib.staticfiles.views import serve
from django.contrib.auth import views as auth_views
from yadlyad.admin import admin_site
from . import views

urlpatterns = [
    # Examples:
    url(r'^$', views.home, name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^static/(?P<path>.*)/', serve),
    url(r'^orders/', include('order.urls', namespace="orders")),
    # url(r'^deliveries/', include('order_delivery.urls', namespace="deliveries")),
    url(r'^accounts/login/', auth_views.login, {'template_name': 'yadlyad/login.html'},  name="login"),
    url(r'^logout/', auth_views.logout_then_login, {'login_url': '/orders/','current_app': 'orders:order'}, name="logout"),
    url(r'^admin/', admin_site.urls)
]
