from django.urls import path
from .import views

urlpatterns = [
    path('', views.home_view, name='api-root'),
    path('products/', views.product_list, name='product-list'),
    path('products/info/', views.product_info, name='product-info'),
    path('products/<int:pk>/', views.product_detail),
    path('orders/', views.order_list, name='order-list'),
]