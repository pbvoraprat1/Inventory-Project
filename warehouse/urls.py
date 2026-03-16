from django.urls import path
from .views import LowStockAlertAPIView, ProductDetailAPIView, ProductListAPIView, StockBalanceListAPIView, StockMovementAPIView, StockBalanceAPIView

urlpatterns = [
    path('stock-movements/', StockMovementAPIView.as_view(), name='api-stock-movement'),
    path('products/', ProductListAPIView.as_view(), name='api-product-list'),
    path('products/<uuid:product_id>/', ProductDetailAPIView.as_view(), name='api-product-detail'),
    path('products/<uuid:product_id>/<int:warehouse_id>/', StockBalanceAPIView.as_view(), name='api-stock-balance'),
    path('<int:warehouse_id>/stock-balances/', StockBalanceListAPIView.as_view(), name='api-stock-balance-list'),
    path('dashboard/<int:warehouse_id>/', LowStockAlertAPIView.as_view(), name='api-low-stock-alert'),

]