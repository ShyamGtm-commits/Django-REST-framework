from django.urls import path
from .import views

urlpatterns = [
    path('', views.home_view, name='api-root'),
    path('products/', views.ProductListAPIView.as_view()),
    path('products/info/', views.ProductInfoAPIView.as_view()),
    path('products/<int:product_id>/', views.ProductDetailListAPIView.as_view()),
    path('orders/', views.OrderListAPIVIew.as_view()),
    path('user-orders/', views.UserOrderListAPIVIew.as_view(), name = 'user-orders'),
]