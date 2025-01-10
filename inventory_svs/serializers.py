from rest_framework import serializers
from .models import Product, ProductBatch, ProductBatchCount, Supplier, Manufacturer, ProductBatchLedger

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBatch
        fields = '__all__'

class ProductBatchCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBatchCount
        fields = '__all__'

class ProductBatchLedgerSerializer(serializers.ModelSerializer):
    batch_count = ProductBatchCountSerializer(read_only=True)
    
    class Meta:
        model = ProductBatchLedger
        fields = ['productBatchledger_id', 'productBatch_id', 'order_id',
                 'order_type', 'quantity', 'order_time', 'batch_count']
