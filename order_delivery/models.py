from django.db import models
from django.db.models import Sum
from order.models import Item, Product


class Delivery(models.Model):
    delivery_date = models.DateField('Delivery Date', 'delivery_date')
    total_orders = models.IntegerField('Total Orders', 'total_orders', default=0)
    for_pesach = models.BooleanField('For Pesach', 'for_pesach', default=False)

    class Meta:
        verbose_name_plural = "deliveries"

    def __str__(self):
        del_date = self.delivery_date
        return '{:%A, %B %d, %Y}'.format(del_date)

    def get_order_count(self):
        return self.order_set.count()

    def get_order_items(self):
        items = []
        for order in self.order_set.select_related('delivery'):
            items.append(Item.objects.filter(order=order))
        return items


def get_all_product_totals():
    prod_query_set = Product.objects.annotate(total_ordered=Sum('item__quantity')).order_by('category_id',
                                                                                            'prod_name')
    return prod_query_set.values()
