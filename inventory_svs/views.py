from rest_framework.decorators import api_view
from rest_framework import status
from .models import Product, ProductBatch, ProductBatchCount, ProductBatchLedger, Supplier, Manufacturer
from .serializers import ProductBatchCountSerializer, ProductBatchLedgerSerializer, ProductSerializer, ProductBatchSerializer, SupplierSerializer, ManufacturerSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from backend.utils.base_crud import CRUDMixin
from backend.utils.decorations import atomic_transaction
from backend.utils.api_response import api_response
from backend.enums import OrderType
from django.db.models import F

class ManufacturerViews(CRUDMixin):
    model = Manufacturer
    serializer_class = ManufacturerSerializer
    lookup_field = 'manufacturer_id'

@swagger_auto_schema(
    method='post',
    request_body=ManufacturerSerializer,
    responses={201: ManufacturerSerializer},
    tags=['Manufacturer']
)
@api_view(['POST'])
def create_manufacturer(request):
    manufacturer_gstn = request.data.get('manufacturer_gstn', '')
    if Manufacturer.objects.filter(manufacturer_gstn__iexact=manufacturer_gstn).exists():
        return api_response(error="Manufacturer with this gstn already exists", 
                          status_code=status.HTTP_409_CONFLICT)
    return ManufacturerViews().create(request)

@swagger_auto_schema(
    method='get',
    responses={200: ManufacturerSerializer(many=True)},
    tags=['Manufacturer']
)
@api_view(['GET'])
def get_all_manufacturers(request):
    return ManufacturerViews().list(request)

@swagger_auto_schema(
    methods=['get', 'put', 'delete'],
    responses={200: ManufacturerSerializer()},
    tags=['Manufacturer']
)
@api_view(['GET', 'PUT', 'DELETE'])
def manufacturer_detail(request, pk=None):
    return ManufacturerViews().retrieve_update_delete(request, pk)

class SupplierViews(CRUDMixin):
    model = Supplier
    serializer_class = SupplierSerializer
    lookup_field = 'supplier_id'

@swagger_auto_schema(
    method='post',
    request_body=SupplierSerializer,
    responses={201: SupplierSerializer},
    tags=['Supplier']
)
@api_view(['POST'])
def create_supplier(request):
    supplier_gstn = request.data.get('supplier_gstn', '')
    if Supplier.objects.filter(supplier_gstn__iexact=supplier_gstn).exists():
        return api_response(error="Supplier with this gst already exists", 
                          status_code=status.HTTP_409_CONFLICT)
    return SupplierViews().create(request)

@swagger_auto_schema(
    method='get',
    responses={200: SupplierSerializer(many=True)},
    tags=['Supplier']
)
@api_view(['GET'])
def get_all_suppliers(request):
    return SupplierViews().list(request)

@swagger_auto_schema(
    methods=['get', 'put', 'delete'],
    responses={200: SupplierSerializer()},
    tags=['Supplier']
)
@api_view(['GET', 'PUT', 'DELETE'])
def supplier_detail(request, pk=None):
    return SupplierViews().retrieve_update_delete(request, pk)

class ProductViews(CRUDMixin):
    model = Product
    serializer_class = ProductSerializer
    lookup_field = 'product_id'

@swagger_auto_schema(
    method='post',
    request_body=ProductSerializer,
    responses={201: ProductSerializer},
    tags=['Product']
)
@api_view(['POST'])
def create_product(request):
    product_name = request.data.get('product_name', '')
    if Product.objects.filter(product_name__iexact=product_name).exists():
        return api_response(error="Product with this name already exists", 
                          status_code=status.HTTP_409_CONFLICT)
    return ProductViews().create(request)

@swagger_auto_schema(
    method='get',
    responses={200: ProductSerializer(many=True)},
    tags=['Product']
)
@api_view(['GET'])
def get_all_products(request):
    return ProductViews().list(request)

@swagger_auto_schema(
    methods=['get', 'put', 'delete'],
    responses={200: ProductSerializer()},
    tags=['Product']
)
@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, pk=None):
    return ProductViews().retrieve_update_delete(request, pk)

## Product Batch Views
class ProductBatchViews(CRUDMixin):
    model = ProductBatch
    serializer_class = ProductBatchSerializer
    lookup_field = 'productBatch_id'

@swagger_auto_schema(
    method='post',
    request_body=ProductBatchSerializer,
    responses={201: ProductBatchSerializer},
    tags=['Product Batch']
)
@api_view(['POST'])
@atomic_transaction()
def create_product_batch(request):
    if ProductBatch.objects.filter(
        org_id=request.data['org_id'],
        sku_id=request.data['sku_id'],
    ).exists():
        return api_response(error="Product already stored in the given SKU", 
                          status_code=status.HTTP_409_CONFLICT)
    return ProductBatchViews().create(request)

@swagger_auto_schema(
    method='get',
    responses={200: ProductBatchSerializer(many=True)},
    tags=['Product Batch']
)
@api_view(['GET'])
def get_all_product_batch(request):
    return ProductBatchViews().list(request)

@swagger_auto_schema(
    methods=['get', 'put', 'delete'],
    responses={200: ProductBatchSerializer()},
    tags=['Product Batch']
)
@api_view(['GET', 'PUT', 'DELETE'])
def product_batch_detail(request, pk=None):
    return ProductBatchViews().retrieve_update_delete(request, pk)

## Product Batch Count Views
class ProductBatchCountViews(CRUDMixin):
    model = ProductBatchCount
    serializer_class = ProductBatchCountSerializer
    lookup_field = 'productBatch_id'

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={'quantity': openapi.Schema(type=openapi.TYPE_NUMBER)}
    ),
    responses={200: ProductBatchCountSerializer()},
    tags=['Product Batch Count']
)
@api_view(['POST'])
@atomic_transaction()
def add_product_batch_quantity(request, productBatch_id):
    quantity = request.data.get('quantity')
    if quantity is None:
        return api_response(error="Quantity is required", status_code=status.HTTP_400_BAD_REQUEST)
    
    try:
        batch_count = ProductBatchCount.objects.filter(productBatch_id=productBatch_id).first()
        
        if batch_count:  # If it exists, update the available_quantity
            batch_count.available_quantity += quantity
        else:  # If not, create a new ProductBatchCount with the given quantity
            batch_count = ProductBatchCount.objects.create(
                productBatch_id=productBatch_id,
                available_quantity=quantity
            )
        batch_count.save()
        
        ProductBatchLedger.objects.create(
            productBatch_id=productBatch_id,
            order_id='9e23e8a2-124d-5fd9-9f2b-28c7a881d740',
            order_type=OrderType.STOCK_ENTRY.value,
            quantity=quantity,
        )
        
        return api_response(ProductBatchCountSerializer(batch_count).data)
    except ProductBatchCount.DoesNotExist:
        return api_response(error="Invalid productBatch_id", status_code=status.HTTP_404_NOT_FOUND)
    
@swagger_auto_schema(
    method='get',
    responses={200: ProductBatchCountSerializer(many=True)},
    tags=['Product Batch Count']
)
@api_view(['GET'])
def get_all_product_batch_count(request):
    return ProductBatchCountViews().list(request)

@swagger_auto_schema(
    methods=['get', 'put', 'delete'],
    responses={200: ProductBatchCountSerializer()},
    tags=['Product Batch Count']
)
@api_view(['GET', 'PUT', 'DELETE'])
def product_batch_count_detail(request, pk=None):
    return ProductBatchCountViews().retrieve_update_delete(request, pk)

## Product Batch Ledger Views
@swagger_auto_schema(
    method='get',
    responses={200: ProductBatchLedgerSerializer(many=True)},
    tags=['Product Batch']
)
@api_view(['GET'])
def get_batch_ledger(request, productBatch_id):
    ProductBatch.objects.get(productBatch_id=productBatch_id)
    ledger_entries = ProductBatchLedger.objects.filter(productBatch_id=productBatch_id)
    return api_response(ProductBatchLedgerSerializer(ledger_entries, many=True).data)