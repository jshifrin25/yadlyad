from django.db import models


# Create your models here.


class Category(models.Model):
    cat_name = models.CharField('Category Name', max_length=50)
    cat_description = models.CharField('Category Description', max_length=200)

    def __str__(self):
        return self.cat_name

    class Meta:
        verbose_name_plural = 'Categories'


class Product(models.Model):
    prod_name = models.CharField('Product Name', max_length=50)
    prod_description = models.CharField('Product Description', max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    pesach_only = models.BooleanField(default=False)
    pesach_and_year = models.BooleanField('Pesach and the year too', default=True)
    weight_in_pounds = models.FloatField(default=0.0)
    limit = models.IntegerField(default=0)

    def __str__(self):
        return self.prod_name


class Order(models.Model):
    recipient = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    date_created = models.DateField('Creation Date', auto_now=True)
    delivery = models.ForeignKey('order_delivery.Delivery', on_delete=models.CASCADE, blank=True, null=True)
    
    def clone_for_newdelivery(self,  delivery):
        order = Order(
             recipient = self.recipient, 
             delivery = delivery
        )
        order.save()
        for item in self.item_set.all():
            order.item_set.create(
                product = item.product, 
                quantity = item.quantity
            )
        return order

    def __str__(self):
        return 'Order #' + str(self.pk) + ' was made by User ' + str(self.recipient)


class Item(models.Model):
    quantity = models.PositiveSmallIntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return 'Item Id: ' + str(self.pk) + ' :' + self.product.prod_name + ' quantity: ' + str(self.quantity)

