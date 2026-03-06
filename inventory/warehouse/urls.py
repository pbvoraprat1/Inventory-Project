from django.urls import path
from .views import StockMovementAPIView

urlpatterns = [
    path('stock-movements/', StockMovementAPIView.as_view(), name='api-stock-movement'),
]