
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from django.core.cache import cache

from apps.products.models import Product

class ProductSearch(APIView):

    def get(self,request):

        q = request.GET.get('q','')

        key = f"search_{q}"

        cached = cache.get(key)
        if cached:
            return Response(cached)

        qs = Product.objects.filter(
            Q(title__icontains=q)|
            Q(description__icontains=q)|
            Q(category__name__icontains=q)
        )

        data = list(qs.values('id','title','price'))

        cache.set(key,data,60)

        return Response(data)


class AutoComplete(APIView):

    def get(self,request):

        q = request.GET.get('q','')

        if len(q)<3:
            return Response([])

        qs = Product.objects.filter(title__istartswith=q)[:10]

        return Response(list(qs.values_list('title',flat=True)))
