
from django.db import models
from apps.products.models import Product

class Store(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Inventory(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    low_stock_limit = models.PositiveIntegerField(default=5)   




    class Meta:
        unique_together = ['store','product']

    def is_low_stock(self):
        return self.quantity <= self.low_stock_limit