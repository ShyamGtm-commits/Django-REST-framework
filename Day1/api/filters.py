import django_filters
from api.models import Product

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'name': ['iexact', 'icontains'], # insertion of the i in the exact and other make it discard the case sensitive issue 
            'price': ['exact', 'lt', 'gt', 'range']
        }
