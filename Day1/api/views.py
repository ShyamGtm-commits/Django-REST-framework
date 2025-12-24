from django.db.models import Max
from django.shortcuts import get_object_or_404
from api.serializers import ProductSerializer, OrderSerializer, ProductInfoSerializer
from api.models import Product, Order, OrderItem
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import generics
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    AllowAny
    )
from rest_framework.views import APIView
from api.filters import ProductFilter, InStockFilterBackend
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

@api_view(['GET'])
def home_view(request):
    return Response({
        'message': 'Welcome to My DRF API',
        'endpoints': {
            'products_list': reverse('product-list', request=request),
            'products_info': reverse('product-info', request=request),
            'orders_list': reverse('order-list', request=request),
        },
        'instructions': 'Use these endpoints to interact with the API'
    })


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.order_by('pk')
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = [
        DjangoFilterBackend, 
        filters.SearchFilter,
        filters.OrderingFilter,
        InStockFilterBackend
    ]
    search_fields = ['name', 'description']

    ordering_filters = ['name', 'price', 'stock']
    pagination_class = LimitOffsetPagination
    # pagination_class.page_size = 2 
    # pagination_class.page_query_param = 'pagenum'
    # pagination_class.page_size_query_param = 'page_size'
    # pagination_class.max_page_size = 6

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


# @api_view(['GET'])
# def product_list(request):
#     products = Product.objects.all()
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)


class ProductDetailUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id'

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

# @api_view(['GET'])
# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     serializer = ProductSerializer(product)
#     return Response(serializer.data)


class OrderListAPIVIew(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer


class UserOrderListAPIVIew(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)


# @api_view(['GET'])
# def order_list(request):
#     orders = Order.objects.prefetch_related(  # here the prefetch_related is used to reduce the time taken to make the queries and the queries numbers are reduced that were made bigger by the nested serializer
#             'items__product' # items__product is another one that makes this possible and reduces the nested again so we can discard 'items'
#         ) # we can just kill this .all() items too and later on this another one all can also be killed that isn't anything that matters that seriously
#     serializer = OrderSerializer(orders, many=True)
#     return Response(serializer.data)

class ProductInfoAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer({
            'products': products,
            'count': len(products),
            # must get the piece of the aggregated data out of the dictionary by indexing in the key name['max_price]
            'max_price': products.aggregate(max_price=Max('price'))['max_price']
        })
        return Response(serializer.data)

# this is for making the crud functions here in the django rest framework
