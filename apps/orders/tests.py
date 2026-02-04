
from django.test import TestCase
from apps.stores.models import Store,Inventory
from apps.products.models import Category,Product

class OrderTest(TestCase):

    def setUp(self):

        c = Category.objects.create(name="Test")
        p = Product.objects.create(title="P1",price=100,category=c)
        s = Store.objects.create(name="S1",location="X")

        Inventory.objects.create(store=s,product=p,quantity=10)

    def test_inventory(self):

        inv = Inventory.objects.first()
        self.assertEqual(inv.quantity,10)
