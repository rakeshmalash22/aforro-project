
from django.urls import path
from .views import CreateOrder, sales_dashboard

urlpatterns = [

    # API
    path("orders/", CreateOrder.as_view()),

    # Dashboard page
    path("dashboard/", sales_dashboard, name="sales_dashboard"),
]

