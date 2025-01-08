from rest_framework.decorators import api_view
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

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
def add_provision_order_item(request):
    # Validate order batch and its status
    order_batch = OrderBatch.objects.get(orderBatch_id=request.data['orderBatch_id'])
    OrderValidator.validate_provision_order(order_batch)
    OrderValidator.validate_duplicate_order_item(
        request.data['orderBatch_id'],
        request.data['productBatch_id']
    )
    # Validate product availability
    OrderValidator.validate_product_availability(
        request.data['productBatch_id'], 
        request.data['order_quantity']
    )
    
    # Process order details
    order_details = OrderService.process_order_item(request.data)
    
    # Prepare order item data
    order_item_data = OrderService.prepare_order_item_data(
        request.data,
        orderBatch_id=request.data['orderBatch_id'],
        product=order_details['product'],
        price_per_unit=order_details['price_per_unit'],
        total_price=order_details['total_price']
    )
    
    # Create order item
    serializer = OrderItemSerializer(data=order_item_data)
    serializer.is_valid(raise_exception=True)
    order_item = serializer.save()
    
    OrderService.update_order_batch_total(
        request.data['orderBatch_id'], 
        order_details['total_price']
    )
    return api_response(
        OrderItemSerializer(order_item).data, 
        status_code=status.HTTP_201_CREATED
    )

@swagger_auto_schema(
    method='delete',
    responses={204: "No Content"}
)
@api_view(['DELETE'])
@atomic_transaction()
def delete_provision_order_item(request, order_id):
    order_item = OrderValidator.validate_order_item(order_id)
    OrderService.update_order_batch_total(order_item.orderBatch_id, -order_item.total_price)
    order_item.delete()
    return api_response(status_code=status.HTTP_204_NO_CONTENT)

@swagger_auto_schema(
    method='put',
    responses={200: OrderItemSerializer()},
    request_body=OrderItemSerializer
)
@api_view(['PUT'])
@atomic_transaction()
def update_provision_order_item(request, order_id):
    order_item = OrderValidator.validate_order_item(order_id)
    OrderValidator.validate_product_availability(request.data['productBatch_id'], request.data['order_quantity'])
    
    order_details = OrderService.process_order_item(request.data)
    order_item_data = OrderService.prepare_order_item_data(
        request.data,
        price_per_unit=order_details['price_per_unit'],
        total_price=order_details['total_price'],
        is_update=True
    )
    
    serializer = OrderItemSerializer(order_item, data=order_item_data, partial=True)
    if serializer.is_valid():
        updated_item = serializer.save()
        OrderService.update_order_batch_total(order_item.orderBatch_id, order_details['total_price'], order_item.total_price)
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