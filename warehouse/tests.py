from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Category, Product, Warehouse, StockBalance, StockTransaction
from .services import perform_stock_transaction
from django.core.exceptions import ValidationError

class StockMovementTests(TestCase):
    
    def setUp(self):
        """
        ฟังก์ชันนี้จะทำงานอัตโนมัติก่อนเริ่มเทสเสมอ
        หน้าที่ของมันคือ 'สร้างข้อมูลจำลองใน Database ชั่วคราว'
        """
        self.user = User.objects.create(username="tester_admin")
        self.cat = Category.objects.create(name="Electronics")
        self.prod = Product.objects.create(sku="IPHONE-15", name="iPhone 15 Pro", category=self.cat, base_price=35000)
        self.wh = Warehouse.objects.create(code="WH-BKK", name="คลังสินค้ากรุงเทพ")

    def test_stock_in_success(self):
        """เทสที่ 1: ทดสอบการรับของเข้า 10 ชิ้น"""
        perform_stock_transaction(
            product=self.prod, warehouse=self.wh, user=self.user,
            transaction_type=StockTransaction.TransactionType.IN, quantity=10
        )
        
        # ไปดึงยอดคงเหลือมาเช็คว่าเท่ากับ 10 จริงไหม
        balance = StockBalance.objects.get(product=self.prod, warehouse=self.wh)
        self.assertEqual(balance.quantity, 10) # เช็คความถูกต้อง

    def test_stock_out_insufficient(self):
        """เทสที่ 2: ทดสอบระบบป้องกันการเบิกของเกินสต็อก (ต้องเกิด Error)"""
        # ใช้ with self.assertRaises เพื่อบอกว่า "บรรทัดถัดไปต้องเกิด ValidationError นะ ถึงจะแปลว่าระบบป้องกันทำงานถูกต้อง"
        with self.assertRaises(ValidationError):
            perform_stock_transaction(
                product=self.prod, warehouse=self.wh, user=self.user,
                transaction_type=StockTransaction.TransactionType.OUT, quantity=50 # ของมี 0 แต่จะเบิก 50
            )