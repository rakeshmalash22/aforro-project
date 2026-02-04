
from django.urls import path
from .views import ProductSearch,AutoComplete

urlpatterns = [
 path('search/products/',ProductSearch.as_view()),
 path('search/suggest/',AutoComplete.as_view()),
]
