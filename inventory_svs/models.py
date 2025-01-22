import uuid
from django.db import models
from datetime import datetime, timedelta

from backend.enums import OrderType, UnitType

class Manufacturer(models.Model):
    manufacturer_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    org_id = models.UUIDField(db_index=True)
    manufacturer_name = models.TextField()
    manufacturer_contact_person = models.TextField()
    manufacturer_email = models.TextField()
    manufacturer_contact_number = models.TextField()
    manufacturer_address = models.TextField()
    manufacturer_gstn = models.TextField()

    def __str__(self):
        return self.manufacturer_name

class Supplier(models.Model):
    supplier_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    org_id = models.UUIDField(db_index=True)
    supplier_name = models.TextField()
    supplier_contact_person = models.TextField()
    returnable = models.BooleanField(default=False)
    supplier_email = models.TextField()
    supplier_contact_number = models.TextField()
    supplier_address = models.TextField()
    supplier_gstn = models.TextField()

    def __str__(self):
        return self.supplier_name

class Product(models.Model):
    product_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    org_id = models.UUIDField(db_index=True)
    manufacturer_id = models.UUIDField()
    product_name = models.TextField()
    product_desc = models.TextField(help_text='Content of the post')
    product_type = models.TextField()
    product_packaging = models.TextField()
    product_measurement_unit = models.CharField(max_length=20, choices=UnitType.choices()) 

    def __str__(self):
        return self.product_name

class ProductBatch(models.Model):
    productBatch_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    org_id = models.UUIDField(db_index=True)
    product_id = models.UUIDField(db_index=True)
    productBatch_created_date = models.DateTimeField(default=(datetime.now))
    productBatch_cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    productBatch_mrp = models.DecimalField(max_digits=10, decimal_places=2)
    productBatch_discount = models.DecimalField(max_digits=10, decimal_places=2)
    productBatch_currentOffers = models.CharField(max_length=100)
    productBatch_created_by = models.DateTimeField(default=datetime.now)
    productBatch_supplier_ID = models.CharField(max_length=100)
    sku_id = models.CharField(max_length=100)
    productBatch_DateOfManufacture = models.DateField()
    productBatch_DateOfExpiry = models.DateField(default=(datetime.today() + timedelta(days=36500)).date())

    def __str__(self):
        return f"{self.product.product_name} - Batch {self.productBatch_id}"
    
class ProductBatchCount(models.Model):
    productBatch_id = models.UUIDField(ProductBatch, db_index=True)
    available_quantity = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.product_name} - Batch {self.productBatch_id}"
    
class ProductBatchLedger(models.Model):
    productBatchledger_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    productBatch_id = models.UUIDField(ProductBatch, db_index=True)
    order_id = models.UUIDField()
    order_type = models.CharField(max_length=20, choices=OrderType.choices())  
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    order_time = models.DateTimeField(default=(datetime.now))

    def __str__(self):
        return f"{self.product.product_name} - Batch {self.productBatch_id}"