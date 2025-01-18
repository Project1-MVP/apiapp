from decimal import Decimal
from rest_framework.decorators import api_view
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from backend.utils.base_crud import CRUDMixin

from .serializers import OrderBatchSerializer, OrderItemSerializer
from .models import OrderBatch, OrderItem

from orders_svs.services import OrderService
from orders_svs.validators import OrderValidator

from backend.utils.decorations import atomic_transaction
from backend.utils.api_response import api_response

##API Calls
@swagger_auto_schema(
    method='post',
    responses={201: OrderBatchSerializer()},
    request_body=OrderBatchSerializer
)
@api_view(['POST'])
@atomic_transaction()
def create_provision_order_batch(request):
    order_batch_data = OrderService.create_provision_order(request.data)
    serializer = OrderBatchSerializer(data=order_batch_data)
    if serializer.is_valid():
        order_batch = serializer.save()
        return api_response(OrderBatchSerializer(order_batch).data, status_code=status.HTTP_201_CREATED)
    return api_response(error=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='post',
    responses={201: OrderItemSerializer()},
    request_body=OrderItemSerializer
)
@api_view(['POST'])
@atomic_transaction()
@api_view(['POST'])
@atomic_transaction()
def add_provision_order_item(request):
    data = request.data
    data['order_quantity'] = Decimal(str(data['order_quantity']))
    order_batch = OrderBatch.objects.get(orderBatch_id=request.data['orderBatch_id'])
    OrderValidator.validate_provision_order(order_batch)
    
    existing_item = OrderValidator.validate_duplicate_order_item(data['orderBatch_id'], data['productBatch_id'])
    if existing_item:
        # Update existing item quantity and recalculate prices
        data['order_quantity'] += existing_item.order_quantity
        OrderValidator.validate_product_availability(data['productBatch_id'], data['order_quantity'])
        order_details = OrderService.process_order_item(data)
        order_item_data = OrderService.prepare_order_item_data(
            data,
            price_per_unit=order_details['price_per_unit'],
            total_price=order_details['total_price'],
            is_update=True
        )
        serializer = OrderItemSerializer(existing_item, data=order_item_data, partial=True)
    else:
        # Create new order item
        OrderValidator.validate_product_availability(data['productBatch_id'], data['order_quantity'])
        order_details = OrderService.process_order_item(data)
        order_item_data = OrderService.prepare_order_item_data(
            data,
            orderBatch_id=data['orderBatch_id'],
            product=order_details['product'],
            price_per_unit=order_details['price_per_unit'],
            total_price=order_details['total_price'],
            quantity_type=OrderService.get_product_quantity_type(data['productBatch_id'])
        )
        serializer = OrderItemSerializer(data=order_item_data)
    
    serializer.is_valid(raise_exception=True)
    order_item = serializer.save()
    OrderService.update_order_batch_total(data['orderBatch_id'])
    return api_response(OrderItemSerializer(order_item).data, status_code=status.HTTP_201_CREATED)
    

@swagger_auto_schema(
    method='delete',
    responses={204: "No Content"}
)
@api_view(['DELETE'])
@atomic_transaction()
def delete_provision_order_item(request, order_id):
    order_item = OrderValidator.validate_order_item(order_id)
    order_item.delete()
    OrderService.update_order_batch_total(order_item.orderBatch_id)
    return api_response(status_code=status.HTTP_204_NO_CONTENT)

@swagger_auto_schema(
    method='put',
    responses={200: OrderItemSerializer()},
    request_body=OrderItemSerializer
)
@api_view(['PUT'])
@atomic_transaction()
def update_provision_order_item(request, order_id):
    data = request.data
    data['order_quantity'] = Decimal(str(data['order_quantity']))
    order_item = OrderValidator.validate_order_item(order_id)
    OrderValidator.validate_product_availability(data['productBatch_id'], data['order_quantity'])
    order_details = OrderService.process_order_item(data)
    order_item_data = OrderService.prepare_order_item_data(
        request.data,
        price_per_unit=order_details['price_per_unit'],
        total_price=order_details['total_price'],
        is_update=True
    )
    serializer = OrderItemSerializer(order_item, data=order_item_data, partial=True)
    if serializer.is_valid():
        updated_item = serializer.save()
        print(order_item.orderBatch_id)
        OrderService.update_order_batch_total(order_item.orderBatch_id)
        return api_response(OrderItemSerializer(updated_item).data)
    return api_response(error=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='post',
    responses={201: OrderBatchSerializer()}
)
@api_view(['POST'])
@atomic_transaction()
def checkout_provision_order_batch(request, orderBatch_id):
    order_batch = OrderBatch.objects.get(orderBatch_id=orderBatch_id)
    OrderValidator.validate_provision_order(order_batch)
    OrderService.update_order_batch_status(order_batch)
    order_items = OrderItem.objects.filter(orderBatch_id=orderBatch_id).all()
    billing_response = OrderService.process_checkout(order_batch, order_items)
    return api_response(billing_response, status_code=status.HTTP_201_CREATED)