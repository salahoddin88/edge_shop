from django.db import models
from django.contrib.auth.models import User
from product.models import Product


class Order(models.Model):
    """ Order Model """
    order_status_choices = (
        ('Pending', 'Pending'),
        ('Inprogress', 'Inprogress'),
        ('Cancelled', 'Cancelled'),
        ('Delivered', 'Delivered')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.TextField()
    date_time = models.DateTimeField()
    payment_status = models.BooleanField(default=False)
    order_status = models.CharField(max_length=255, choices=order_status_choices, default='Pending')

    def __str__(self):
        return str(self.id)


class OrderDetail(models.Model):
    """ Order Details """
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.order.id} - {self.product}'


