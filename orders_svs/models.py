import uuid
from django.db import models
from django.utils import timezone
from backend.enums import OrderStatus, PaymentStatus, UnitType, UserRoles, OrderType, PaymentType, DispatchType

class OrderBatch(models.Model):
    orderBatch_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    org_id = models.UUIDField(db_index=True)
    user_id = models.UUIDField(db_index=True)
    updated_at = models.IntegerField(default=int(timezone.now().timestamp()))
    created_at = models.IntegerField(default=int(timezone.now().timestamp()))  
    order_type = models.CharField(max_length=20, choices=OrderType.choices())
    total_order_value = models.DecimalField(max_digits=10, decimal_places=2)
    dispatch_type = models.CharField(max_length=20, choices=DispatchType.choices())
    payment_type = models.CharField(max_length=20, choices=PaymentType.choices())
    payment_status = models.CharField(max_length=20, choices=PaymentStatus.choices())
    payment_id = models.UUIDField(default='a2d5a8d6-bccf-5b26-b0e9-4b5ab8cf38f1')

    def __str__(self):
        return f"{self.orderBatch_id} - {self.org_id}"

class OrderItem(models.Model):
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    orderBatch_id = models.UUIDField(db_index=True)
    org_id = models.UUIDField(db_index=True)
    order_status = models.CharField(max_length=20, choices=OrderStatus.choices(), default=OrderStatus.PROVISIONING)
    productBatch_id = models.UUIDField()
    order_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_type = models.CharField(max_length=20, choices=UnitType.choices())
    planned_delivery = models.DateField()
    actual_delivery = models.DateTimeField(default=timezone.now() + timezone.timedelta(days=365))
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.orderitem_id} - {self.orderBatch_id}"
    