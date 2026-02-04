
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction

from .models import Order, OrderItem
from apps.stores.models import Inventory, Store
from apps.products.models import Product

class CreateOrder(APIView):

    def post(self,request):

        data = request.data
        store = Store.objects.get(id=data['store_id'])

        items = data['items']
        order = Order.objects.create(store=store,status='PENDING')

        with transaction.atomic():

            for i in items:

                product = Product.objects.get(id=i['product_id'])
                qty = i['quantity']

                inv = Inventory.objects.get(store=store,product=product)

                if inv.quantity < qty:
                    order.status='REJECTED'
                    order.save()
                    return Response({'status':'REJECTED'})

            for i in items:
                product = Product.objects.get(id=i['product_id'])
                qty = i['quantity']
                inv = Inventory.objects.get(store=store,product=product)

                inv.quantity -= qty
                inv.save()

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity_requested=qty
                )

            order.status='CONFIRMED'
            order.save()

        return Response({'status':'CONFIRMED','order_id':order.id})

from django.shortcuts import render
from django.utils import timezone
from .models import Order


def sales_dashboard(request):

    today = timezone.now().date()

    today_orders = Order.objects.filter(
        status="CONFIRMED",
        created_at__date=today
    )

    today_sales = sum(o.get_total_price() for o in today_orders)

    total_sales = sum(
        o.get_total_price()
        for o in Order.objects.filter(status="CONFIRMED")
    )

    recent_orders = Order.objects.filter(status="CONFIRMED").order_by("-created_at")[:5]


    context = {
        "today_sales": today_sales,
        "total_sales": total_sales,
        "today_orders": today_orders.count(),
        "recent_orders": recent_orders,

    }

    return render(request, "orders/dashboard.html", context)
