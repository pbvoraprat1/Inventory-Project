import uuid
from django.db import transaction
from django.core.exceptions import ValidationError
from warehouse.models import Product, Warehouse, StockBalance, StockTransaction


def perform_stock_transaction(product, warehouse, quantity, transaction_type, user, reference_document=""):
    if quantity <= 0:
        raise ValidationError("จำนวนสินค้าต้องมากกว่า 0 !")
    with transaction.atomic():
        balance_obj,created = StockBalance.objects.select_for_update().get_or_create(
            product=product, 
            warehouse=warehouse, 
            defaults={'quantity': 0}
        )
        balance_before = balance_obj.quantity
        if transaction_type == StockTransaction.TransactionType.IN:
            balance_after = balance_before + quantity
        elif transaction_type == StockTransaction.TransactionType.OUT:
            balance_after = balance_before - quantity
            if balance_after < 0:
                raise ValidationError(f"ยอดคงเหลือไม่เพียงพอ! (คงเหลือ: {balance_before}, ต้องการเบิก: {quantity})")
        elif transaction_type == StockTransaction.TransactionType.ADJ:
            balance_after = quantity
            quantity = abs(balance_after - balance_before)
        balance_obj.quantity = balance_after
        balance_obj.save()
        transaction_record = StockTransaction.objects.create(
            transactions_id=f"TXN-{uuid.uuid4().hex[:8].upper()}",
            product=product,
            warehouse=warehouse,
            created_by=user,
            transaction_type=transaction_type,
            quantity=quantity,
            balance_before=balance_before,
            balance_after=balance_after,
            reference_document=reference_document
        )
        return transaction_record

    


    