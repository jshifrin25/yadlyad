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
    fields = ('delivery_date',)
    inlines = [OrderInline]

    def display_order_count(self, obj):
        return obj.get_order_count()

    display_order_count.short_description = 'Number of Orders'
