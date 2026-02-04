
from django.core.management.base import BaseCommand
from faker import Faker

from apps.products.models import Category,Product
from apps.stores.models import Store,Inventory

import random

class Command(BaseCommand):

    def handle(self,*args,**kwargs):

        fake = Faker()

        categories=[]
        for i in range(10):
            categories.append(Category.objects.create(name=fake.word()))

        products=[]
        for i in range(1000):
            products.append(
                Product.objects.create(
                    title=fake.word(),
                    price=random.randint(50,500),
                    category=random.choice(categories)
                )
            )

        stores=[]
        for i in range(20):
            stores.append(Store.objects.create(
                name=fake.company(),
                location=fake.city()
            ))

        for s in stores:
            for p in random.sample(products,300):
                Inventory.objects.create(
                    store=s,
                    product=p,
                    quantity=random.randint(1,50)
                )

        self.stdout.write("Seed Completed")
