from itertools import product

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from .services import perform_stock_transaction
from .serializers import StockBalanceSerializer, StockmovementSerializer, ProductSerializer
from .models import Product, StockBalance, Warehouse, StockTransaction
from rest_framework.permissions import IsAuthenticated

class StockMovementAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = StockmovementSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        try:
            transaction = perform_stock_transaction(
                product=Product.objects.get(id=data['product_id']),       
                warehouse=Warehouse.objects.get(id=data['warehouse_id']),
                quantity=data['quantity'],
                transaction_type=data['transaction_type'],
                user=request.user,
                reference_document=data.get('reference_document', '')
            )
            return Response({
                "message": "ทำรายการสำเร็จเรียบร้อย",
                "transaction_id": transaction.transactions_id, 
                "balance_after": transaction.balance_after
            }, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"สาเหตุที่พัง: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ProductListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        products = Product.objects.filter(is_active=True)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProductDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            serializer = ProductSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response({"error": "ไม่พบสินค้า"}, status=status.HTTP_404_NOT_FOUND)
    def delete(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            product.is_active = False
            product.save()
            return Response({"message": "ลบสินค้าสำเร็จ"}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({"error": "ไม่พบสินค้า"}, status=status.HTTP_404_NOT_FOUND)
    def patch(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            serializer = ProductSerializer(product, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response({"error": "ไม่พบสินค้า"}, status=status.HTTP_404_NOT_FOUND)
        
class StockbalanceAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, product_id, warehouse_id):
        try:
            stock_balance = StockBalance.objects.get(product_id=product_id, warehouse_id=warehouse_id)
            serializer = StockBalanceSerializer(stock_balance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except StockBalance.DoesNotExist:
            return Response({"error": "ไม่พบยอดคงเหลือสำหรับสินค้านี้ในคลังนี้"}, status=status.HTTP_404_NOT_FOUND)
           