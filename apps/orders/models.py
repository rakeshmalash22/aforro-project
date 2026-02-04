from django.db import models
from django.core.exceptions import ValidationError

from apps.products.models import Product
from apps.stores.models import Store, Inventory

class Order(models.Model):

    STATUS = (
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('REJECTED', 'Rejected'),
    )

    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.store.name}"

    def reduce_stock(self):

      for item in self.items.all():

        inventory = Inventory.objects.get(
            store=self.store,
            product=item.product
        )

        # ❌ Check stock
        if inventory.quantity < item.quantity:
            raise ValidationError(
                f"Not enough stock for {item.product}. Available: {inventory.quantity}"
            )

        # ✅ Reduce stock
        inventory.quantity -= item.quantity
        inventory.save()


    def get_total_price(self):
        total = 0

        for item in self.items.all():
            total += item.product.price * item.quantity

        return total



    def save(self, *args, **kwargs):

        old_status = None

        if self.pk:
           old_status = Order.objects.get(pk=self.pk).status

        super().save(*args, **kwargs)

        if self.status == "CONFIRMED" and old_status != "CONFIRMED":
            self.reduce_stock()




class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product} x {self.quantity}"



