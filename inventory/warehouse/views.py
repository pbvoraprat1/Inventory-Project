from itertools import product

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from .services import perform_stock_transaction
from .serializers import StockBalanceSerializer, StockmovementSerializer, ProductSerializer
from .models import Product, StockBalance, Warehouse, StockTransaction
from rest_framework.permissions import IsAuthenticated

#การเคลื่อนไหวของสินค้าในคลัง เช่น รับสินค้าเข้าคลัง, เบิกสินค้า, ปรับยอดคงเหลือ
class StockMovementAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = StockmovementSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        try:
            transaction = perform_stock_transaction(
                product=data['product_id'],       
                warehouse=data['warehouse_id'],
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

#รายการสินค้าทั้งหมดที่มีอยู่ในระบบ(เฉพาะสินค้าที่ is_active = True)    
class ProductListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        products = Product.objects.filter(is_active=True)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#รายละเอียดสินค้าและแก้ไขข้อมูลสินค้า(เช่น ชื่อ, หมวดหมู่, ราคาต้นทุน) และลบสินค้า(ทำให้ is_active = False)
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

#ยอดคงเหลือสินค้าในคลังที่ระบุ      
class StockBalanceAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, product_id, warehouse_id):
        try:
            stock_balance = StockBalance.objects.get(product_id=product_id, warehouse_id=warehouse_id)
            serializer = StockBalanceSerializer(stock_balance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except StockBalance.DoesNotExist:
            return Response({"error": "ไม่พบยอดคงเหลือสำหรับสินค้านี้ในคลังนี้"}, status=status.HTTP_404_NOT_FOUND)

#ยอดคงเหลือสินค้าในคลังทั้งหมดในคลังที่ระบุ       
class StockBalanceListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, warehouse_id):
        try:
            warehouse = Warehouse.objects.get(id=warehouse_id)
        except Warehouse.DoesNotExist:
            return Response({"error": "ไม่มีคลังสินค้านี้"}, status=status.HTTP_404_NOT_FOUND)
        stock_balances = StockBalance.objects.filter(warehouse_id=warehouse_id)
        if not stock_balances.exists():
            return Response({"error": "ไม่พบยอดคงเหลือสำหรับคลังนี้"}, status=status.HTTP_404_NOT_FOUND)
        serializer = StockBalanceSerializer(stock_balances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
       
