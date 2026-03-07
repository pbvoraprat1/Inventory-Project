from django.urls import path
from .views import ProductListAPIView, StockMovementAPIView

urlpatterns = [
    path('stock-movements/', StockMovementAPIView.as_view(), name='api-stock-movement'),
    path('products/', ProductListAPIView.as_view(), name='api-product-list'),
]