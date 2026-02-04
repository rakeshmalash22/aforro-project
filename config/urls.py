
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse


def home(request):
    return HttpResponse("Aforro Project is Running 🚀")


urlpatterns = [

    path('', home),

    path('admin/', admin.site.urls),

    # Orders Dashboard + API
    path('orders/', include('apps.orders.urls')),

    # API only
    path('api/search/', include('apps.search.urls')),
    path('api/stores/', include('apps.stores.urls')),
]

