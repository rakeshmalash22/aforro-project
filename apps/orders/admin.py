from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'store',
        'status',
        'created_at',
        'total_price'
    )

    inlines = [OrderItemInline]

    def total_price(self, obj):
        return obj.get_total_price()

    total_price.short_description = "Total Price"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = ('order', 'product', 'quantity')







