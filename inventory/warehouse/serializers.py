from rest_framework import serializers
from .models import Warehouse, StockBalance, StockTransaction

#API สำหรับจัดการคลังสินค้า
class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'
        
#API สำหรับแสดงยอดคงเหลือสินค้าในคลัง
class StockBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockBalance
        fields = '__all__'

#API สำหรับแสดงรายการการเคลื่อนไหวสินค้าในคลัง(read-only)
class StockTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockTransaction
        fields = '__all__'

#API เอาไว้สำหรับตรวจ json
class StockmovementSerializer(serializers.Serializer):
    product_id = serializers.UUIDField(required=True)
    warehouse_id = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField(min_value=1, required=True)
    transaction_type = serializers.ChoiceField(choices=StockTransaction.TransactionType.choices)
    reference_document = serializers.CharField(max_length=255, required=False, allow_blank=True)