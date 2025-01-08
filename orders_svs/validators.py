from backend.enums import OrderType
from inventory_svs.models import ProductBatchCount
from .models import OrderItem


class OrderValidator:
    @staticmethod
    def validate_provision_order(order_batch):
        if order_batch.order_type != OrderType.PROVISIONING.name:
            raise ValueError("Order must be in PROVISIONING state")

    @staticmethod
    def validate_order_item(order_id):
        order_item = OrderItem.objects.get(order_id=order_id)
        if not order_item:
            raise ValueError("Order item not found")
        return order_item
    
    @staticmethod
    def validate_product_availability(productBatch_id, order_quantity):
        product_batch_count = ProductBatchCount.objects.filter(productBatch_id=productBatch_id).first()
        if not product_batch_count:
            raise ValueError("Product not found")
        if product_batch_count.available_quantity < order_quantity:
            raise ValueError("Insufficient quantity available")
        return product_batch_count
    
    @staticmethod
    def validate_duplicate_order_item(orderBatch_id, productBatch_id):
        existing_item = OrderItem.objects.filter(
            orderBatch_id=orderBatch_id,
            productBatch_id=productBatch_id
        ).exists()
        if existing_item:
            raise ValueError("This product is already in the order batch")
