from datetime import datetime
from decimal import Decimal
from backend.enums import DispatchType, OrderStatus, OrderType, PaymentStatus
from inventory_svs.models import Product, ProductBatch, ProductBatchCount, ProductBatchLedger
from .models import OrderBatch
from .validators import OrderValidator


class OrderService:
    @staticmethod
    def process_order_item(request_data, orderBatch_id=None):
        product_batch = ProductBatch.objects.get(productBatch_id=request_data['productBatch_id'])
        product = Product.objects.get(product_id=product_batch.product_id)
        price_per_unit, total_price = OrderValidator.calculate_price_details(product_batch, request_data['order_quantity'])
        
        return {
            'product_batch': product_batch,
            'product': product,
            'price_per_unit': price_per_unit,
            'total_price': total_price
        }

    @staticmethod
    def process_billing_item(item):
        return {
            'order_id': item.order_id,
            'product_id': item.productBatch_id,
            'quantity': item.order_quantity,
            'unit_price': item.price_per_unit,
            'total_price': item.total_price
        }

    @staticmethod
    def create_provision_order(data):
        order_batch_data = {
            'org_id': data['org_id'],
            'user_id': data['user_id'],
            'order_type': OrderType.PROVISIONING.name,
            'order_status': OrderStatus.PROVISIONING.name,
            'dispatch_type': DispatchType.STORE.name,
            'payment_type': data['payment_type'].upper(),
            'payment_status': PaymentStatus.UNPAID.name,
            'total_order_value': 0
        }
        return order_batch_data

    @staticmethod
    def process_checkout(order_batch, order_items):
        billing_items = []
        for item in order_items:
            ProductBatchLedger.objects.create(
                productBatch_id=item.productBatch_id,
                order_id=item.order_id,
                order_type=OrderType.PROVISIONING.name,
                quantity=item.order_quantity,
            )
            
            batch_count = ProductBatchCount.objects.get(productBatch_id=item.productBatch_id)
            batch_count.available_quantity -= item.order_quantity
            batch_count.save()
            
            billing_items.append(OrderService.process_billing_item(item))
        
        return {
            'order_batch_id': order_batch.orderBatch_id,
            'total_amount': order_batch.total_order_value,
            'payment_status': PaymentStatus.PAID.name,
            'items': billing_items,
            'timestamp': int(datetime.now().timestamp())
        }

    @staticmethod
    def update_order_batch_status(order_batch):
        order_batch.order_type = OrderType.SALE.name
        order_batch.payment_status = PaymentStatus.PAID.name
        order_batch.updated_at = datetime.now().timestamp()
        order_batch.save()

    @staticmethod
    def prepare_order_item_data(request_data, **kwargs):
        if kwargs.get('is_update'):
            return {
                'order_quantity': request_data['order_quantity'],
                'price_per_unit': kwargs.get('price_per_unit'),
                'total_price': kwargs.get('total_price'),
                'order_status': 'PENDING',
                'planned_delivery': datetime.today().date()
            }
        
        return {
            'org_id': request_data['org_id'],
            'orderBatch_id': kwargs.get('orderBatch_id'),
            'productBatch_id': request_data['productBatch_id'],
            'order_quantity': request_data['order_quantity'],
            'quantity_type': kwargs.get('product').product_measurement_unit,
            'price_per_unit': kwargs.get('price_per_unit'),
            'total_price': kwargs.get('total_price'),
            'order_status': 'PENDING',
            'planned_delivery': datetime.today().date()
        }
    
    @staticmethod
    def update_order_batch_total(orderBatch_id, total_price, subtract_existing=None):
        order_batch = OrderBatch.objects.get(orderBatch_id=orderBatch_id)
        if subtract_existing:
            order_batch.total_order_value = order_batch.total_order_value - subtract_existing + total_price
        else:
            order_batch.total_order_value += total_price
        order_batch.save()
        return order_batch
    
    @staticmethod
    def calculate_price_details(product_batch, order_quantity):
        price_per_unit = Decimal(str(product_batch.productBatch_mrp * (1 - product_batch.productBatch_discount / 100))).quantize(Decimal('0.01'))
        total_price = Decimal(str(order_quantity * price_per_unit)).quantize(Decimal('0.01'))
        return price_per_unit, total_price