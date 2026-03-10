from django.contrib import admin
from .models import Category, Product, Warehouse, StockBalance, StockTransaction
# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'sku', 'name', 'category', 'base_price')
    search_fields = ('sku', 'name')
    list_filter = ('category','is_active')

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name', 'location')
    search_fields = ('code', 'name')

@admin.register(StockBalance)
class StockBalanceAdmin(admin.ModelAdmin):
    list_display = ('product', 'warehouse', 'quantity', 'last_updated')
    search_fields = ('product__name', 'warehouse__name', 'product__sku')
    list_filter = ('warehouse',)
    def has_add_permission(self, request):
        return False

@admin.register(StockTransaction)
class StockTransactionAdmin(admin.ModelAdmin):
    list_display = ('transactions_id', 'product', 'warehouse', 'transaction_type', 'quantity', 'balance_before', 'balance_after', 'created_by', 'timestamp')
    search_fields = ('transactions_id', 'product__name', 'reference_document')
    list_filter = ('transaction_type', 'warehouse','timestamp')
    readonly_fields = ('balance_before', 'balance_after')


