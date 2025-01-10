from django.urls import path
from . import views

urlpatterns = [
    # Manufacturer URLs
    path('manufacturers/', views.get_all_manufacturers, name='get-all-manufacturers'),
    path('manufacturers/create/', views.create_manufacturer, name='create-manufacturer'),
    path('manufacturers/<str:pk>/', views.manufacturer_detail, name='manufacturer-detail'),
    
    # Supplier URLs
    path('suppliers/', views.get_all_suppliers, name='get-all-suppliers'),
    path('suppliers/create/', views.create_supplier, name='create-supplier'),
    path('suppliers/<str:pk>/', views.supplier_detail, name='supplier-detail'),
    
    # Product URLs
    path('products/', views.get_all_products, name='get-all-products'),
    path('products/create/', views.create_product, name='create-product'),
    path('products/<str:pk>/', views.product_detail, name='product-detail'),

    # Product Batch URLs
    path('product-batch/create/', views.create_product_batch, name='create_product_batch'),
    path('product-batch/', views.get_all_product_batch, name='get-all-product-batch'),
    path('product-batch/<str:pk>/', views.product_batch_detail, name='product-batch-detail'),

    #product batch count
    path('product-batch/<uuid:productBatch_id>/add-quantity/', views.add_product_batch_quantity, name='add_product_batch_quantity'),
    path('product-batch-count/', views.get_all_product_batch_count, name='product-batch-count-list'),
    path('product-batch-count/<uuid:pk>/', views.product_batch_count_detail, name='product-batch-count-specific'),

    # Product ledger URLs
    path('batch-ledger/<uuid:productBatch_id>/', views.get_batch_ledger, name='get_batch_ledger'),
]
