from django.contrib import admin
from .models import Order, Product, Category, Item


class ItemInline(admin.TabularInline):
    model = Item
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('display_order_id', 'recipient', 'date_created',)
    list_display_links = ('display_order_id',)
    list_filter = ('delivery',)
    inlines = [ItemInline]

    def display_order_id(self, obj):
        return "%d" % obj.id

    display_order_id.short_description = 'Order ID'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,
         {'fields': ['prod_name', 'prod_description', 'category']}),
        ('Options', {'fields': [('pesach_only', 'pesach_and_year'), 'limit'],
                     'classes': ['collapse', 'small']})
    ]
    list_display = ('prod_name', 'prod_description')
    list_display_links = ('prod_name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ('cat_name', 'cat_description')
