from django.db.models import Max
from django.shortcuts import get_object_or_404
from api.serializers import ProductSerializer, OrderSerializer, ProductInfoSerializer
from api.models import Product, Order, OrderItem
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse  

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

@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)

@api_view(['GET'])
def order_list(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_info(request):
    products = Product.objects.all()
    serializer = ProductInfoSerializer({
        'products': products,
        'count': len(products),
        'max_price': products.aggregate(max_price = Max('price'))['max_price'] #must get the piece of the aggregated data out of the dictionary by indexing in the key name['max_price]
    })
    return Response(serializer.data)