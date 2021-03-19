from django.db import models

# Create your models here.


class Products(models.Model):
    product = models.CharField(max_length=50, blank=True)
    discription = models.TextField(max_length=100)
    price = models.DecimalField(max_digits=7, decimal_places=2)


class Orders(models.Model):
    customer_name = models.CharField(max_length=200, blank=True)
    customer_address = models.TextField(max_length=200, blank=True)
    customer_email = models.EmailField(max_length=100, blank=True)
    customer_mobile = models.IntegerField(max_length=10)
    total_amount = models.DecimalField(max_digits=9, decimal_places=2, blank=False)
    payment_status = models.BooleanField(default=False, blank=False)


class OrderDetails(models.Model):
    name = models.CharField(max_length=50, blank=False)
    price = models.DecimalField(max_digits=9, decimal_places=2, blank=False)
    order = models.ForeignKey(Orders, blank=False, on_delete=models.CASCADE)