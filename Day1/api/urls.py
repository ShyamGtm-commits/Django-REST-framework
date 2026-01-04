from django.urls import path
from .import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    # path('', views.home_view, name='api-root'),
    path('products/', views.ProductListCreateAPIView.as_view()),
    path('products/info/', views.ProductInfoAPIView.as_view()),
    path('products/<int:product_id>/', views.ProductDetailUpdateDestroyAPIView.as_view()),
    path('users/', views.UserListView.as_view()),
    # gonna make the viewsets for the order
]
router = DefaultRouter()
router.register('orders', views.OrderViewSet)
urlpatterns += router.urls