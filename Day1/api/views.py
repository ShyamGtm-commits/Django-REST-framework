from django.db.models import Max
from django.shortcuts import get_object_or_404
from api.serializers import ProductSerializer, OrderSerializer, ProductInfoSerializer
from api.models import Product, Order, OrderItem
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse  
from rest_framework import generics

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

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.filter(stock__gt=0) # filter is used to show the products that only have the stock available and exclude is opposite
    serializer_class = ProductSerializer

# @api_view(['GET'])
# def product_list(request):
#     products = Product.objects.all()
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)

class ProductDetailListAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id'

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

@api_view(['GET'])
def product_info(request):
    products = Product.objects.all()
    serializer = ProductInfoSerializer({
        'products': products,
        'count': len(products),
        'max_price': products.aggregate(max_price = Max('price'))['max_price'] #must get the piece of the aggregated data out of the dictionary by indexing in the key name['max_price]
    })
    return Response(serializer.data)