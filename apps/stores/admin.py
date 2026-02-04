from django.contrib import admin
from .models import Store, Inventory


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):

    list_display = (
        'store',
        'product',
        'quantity',
        'low_stock_limit',
        'low_stock_status',
    )

    def low_stock_status(self, obj):
        if obj.is_low_stock():
            return "⚠️ LOW"
        return "OK ✅"

    low_stock_status.short_description = "Stock Status"


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')

