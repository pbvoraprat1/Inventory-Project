import uuid
from django.db import models
from django.conf import settings

#Category model(หมวดหมู่สินค้า)
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
#Product model(สินค้า)
class Product(models.Model):
    id  = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sku = models.CharField(max_length=100, unique=True,db_index=True)
    name = models.CharField(max_length=255)
    catagory_id = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    reorder_level = models.IntegerField(default=10)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

#Warehouse model(คลังสินค้า)
class Warehouse(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    location = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
#Stock balance model(ยอดคงเหลือสินค้าในคลัง)
class StockBalance(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_balances')
    Warehouse_id = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='stock_balances')
    quantity = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('product_id', 'Warehouse_id')

#Stocktransaction model(การเคลื่อนไหวของสินค้าในคลัง)
class StockTransaction(models.Model):
    class TransactionType(models.TextChoices):
        IN = 'IN', 'Stock In'       #(รับสินค้าเข้าคลัง)
        OUT = 'OUT', 'Stock Out'    #(เบิกสินค้า)
        ADJ = 'ADJ', 'Adjust'       #(ปรับยอดคงเหลือ)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_transactions')
    Warehouse_id = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='stock_transactions')
    transactions_id = models.CharField(max_length=100, unique=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    transaction_type = models.CharField(max_length=3, choices=TransactionType.choices)
    quantity = models.IntegerField()
    balance_before = models.IntegerField(editable=False)
    balance_after = models.IntegerField(editable=False)
    reference_document = models.CharField(max_length=100, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']