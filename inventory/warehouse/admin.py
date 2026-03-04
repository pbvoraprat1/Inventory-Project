from django.contrib import admin
from .models import Category, Product, Warehouse, StockBalance, StockTransaction
# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Warehouse)
admin.site.register(StockBalance)
admin.site.register(StockTransaction)