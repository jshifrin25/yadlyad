from django.contrib import admin
from order_delivery.models import Delivery
from order.models import Order


class OrderInline(admin.TabularInline):
    model = Order
    readonly_fields = ('date_created',)
    ordering = ['recipient']
    extra = 0
    can_delete = True
    min_num = None



@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('delivery_date', 'display_order_count')
    fields = ('delivery_date','for_pesach')
    inlines = [OrderInline]
    actions = ['duplicate_orders']

    def display_order_count(self, obj):
        return obj.get_order_count()
        
    
    def response_add(self,  request,  obj,  post_url_continue=None):
        print(obj)
        return self.response_post_save_add(request,  obj)

    display_order_count.short_description = 'Number of Orders'
