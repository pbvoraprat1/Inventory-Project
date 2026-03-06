from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from .services import perform_stock_transaction
from .serializers import StockmovementSerializer
from .models import Product, Warehouse, StockTransaction

class StockMovementAPIView(APIView):
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
                user=request.user if request.user.is_authenticated else None,
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
