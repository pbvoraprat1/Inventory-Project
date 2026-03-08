from django.urls import path
from .views import ProductDetailAPIView, ProductListAPIView, StockMovementAPIView, StockbalanceAPIView

urlpatterns = [
    path('stock-movements/', StockMovementAPIView.as_view(), name='api-stock-movement'),
    path('products/', ProductListAPIView.as_view(), name='api-product-list'),
    path('products/<uuid:product_id>/', ProductDetailAPIView.as_view(), name='api-product-detail'),
    path('products/<uuid:product_id>/<int:warehouse_id>/', StockbalanceAPIView.as_view(), name='api-stock-balance'),

]