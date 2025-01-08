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

class ManufacturerViews(CRUDMixin):
    model = Manufacturer
    serializer_class = ManufacturerSerializer
    lookup_field = 'manufacturer_id'

@swagger_auto_schema(
    method='post',
    request_body=ManufacturerSerializer,
    responses={201: ManufacturerSerializer}
)
@api_view(['POST'])
def create_manufacturer(request):
    manufacturer_gstn = request.data.get('manufacturer_gstn', '')
    if Manufacturer.objects.filter(manufacturer_gstn__iexact=manufacturer_gstn).exists():
        return api_response(error="Manufacturer with this gstn already exists", 
                          status_code=status.HTTP_409_CONFLICT)
    return ManufacturerViews().create(request)

@api_view(['GET'])
def get_all_manufacturers(request):
    return ManufacturerViews().list(request)

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
    responses={201: SupplierSerializer}
)
@api_view(['POST'])
def create_supplier(request):
    supplier_gstn = request.data.get('supplier_gstn', '')
    if Supplier.objects.filter(supplier_gstn__iexact=supplier_gstn).exists():
        return api_response(error="Supplier with this gst already exists", 
                          status_code=status.HTTP_409_CONFLICT)
    return SupplierViews().create(request)

@api_view(['GET'])
def get_all_suppliers(request):
    return SupplierViews().list(request)

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
    responses={201: ProductSerializer}
)
@api_view(['POST'])
def create_product(request):
    product_name = request.data.get('product_name', '')
    if Product.objects.filter(product_name__iexact=product_name).exists():
        return api_response(error="Product with this name already exists", 
                          status_code=status.HTTP_409_CONFLICT)
    return ProductViews().create(request)

@api_view(['GET'])
def get_all_products(request):
    return ProductViews().list(request)

@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, pk=None):
    return ProductViews().retrieve_update_delete(request, pk)

@swagger_auto_schema(
    method='post',
    request_body=ProductBatchSerializer,
    responses={201: ProductBatchSerializer()}
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
    
    serializer = ProductBatchSerializer(data=request.data)
    if serializer.is_valid():
        product_batch = ProductBatch.objects.create(**serializer.validated_data)
        ProductBatchCount.objects.create(
            productBatch_id=product_batch.productBatch_id,
            available_quantity=0
        )
        return api_response(ProductBatchSerializer(product_batch).data, 
                          status_code=status.HTTP_201_CREATED)
    return api_response(error=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={'quantity': openapi.Schema(type=openapi.TYPE_NUMBER)}
    ),
    responses={200: ProductBatchCountSerializer()}
)
@api_view(['POST'])
@atomic_transaction()
def add_product_batch_quantity(request, productBatch_id):
    quantity = request.data['quantity']
    batch_count, created = ProductBatchCount.objects.get_or_create(
        productBatch_id=productBatch_id,
        defaults={'available_quantity': 0}
    )
    
    batch_count.available_quantity += quantity
    batch_count.save()
    
    ProductBatchLedger.objects.create(
        productBatch_id=productBatch_id,
        order_id='9e23e8a2-124d-5fd9-9f2b-28c7a881d740',
        order_type=OrderType.STOCK_ENTRY.value,
        quantity=quantity,
    )
    
    return api_response(ProductBatchCountSerializer(batch_count).data)

@swagger_auto_schema(
    method='get',
    responses={200: ProductBatchLedgerSerializer(many=True)}
)
@api_view(['GET'])
def get_batch_ledger(request, productBatch_id):
    ProductBatch.objects.get(productBatch_id=productBatch_id)
    ledger_entries = ProductBatchLedger.objects.filter(productBatch_id=productBatch_id)
    return api_response(ProductBatchLedgerSerializer(ledger_entries, many=True).data)