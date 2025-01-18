from django.views.decorators.csrf import ensure_csrf_cookie
from django.urls import path
from . import views

urlpatterns = [
    # Manufacturer URLs
    path('manufacturers/', ensure_csrf_cookie(views.get_all_manufacturers), name='get-all-manufacturers'),
    path('manufacturers/create/', ensure_csrf_cookie(views.create_manufacturer), name='create-manufacturer'),
    path('manufacturers/<str:pk>/', ensure_csrf_cookie(views.manufacturer_detail), name='manufacturer-detail'),
    
    # Supplier URLs
    path('suppliers/', ensure_csrf_cookie(views.get_all_suppliers), name='get-all-suppliers'),
    path('suppliers/create/', ensure_csrf_cookie(views.create_supplier), name='create-supplier'),
    path('suppliers/<str:pk>/', ensure_csrf_cookie(views.supplier_detail), name='supplier-detail'),
    
    # Product URLs
    path('products/', ensure_csrf_cookie(views.get_all_products), name='get-all-products'),
    path('products/create/', ensure_csrf_cookie(views.create_product), name='create-product'),
    path('products/<str:pk>/', ensure_csrf_cookie(views.product_detail), name='product-detail'),

    # Product Batch URLs
    path('product-batch/create/', ensure_csrf_cookie(views.create_product_batch), name='create_product_batch'),
    path('product-batch/', ensure_csrf_cookie(views.get_all_product_batch), name='get-all-product-batch'),
    path('product-batch/<str:pk>/', ensure_csrf_cookie(views.product_batch_detail), name='product-batch-detail'),

    #product batch count
    path('product-batch/<uuid:productBatch_id>/add-quantity/', ensure_csrf_cookie(views.add_product_batch_quantity), name='add_product_batch_quantity'),
    path('product-batch-count/', ensure_csrf_cookie(views.get_all_product_batch_count), name='product-batch-count-list'),
    path('product-batch-count/<uuid:pk>/', ensure_csrf_cookie(views.product_batch_count_detail), name='product-batch-count-specific'),

    # Product ledger URLs
    path('batch-ledger/<uuid:productBatch_id>/', ensure_csrf_cookie(views.get_batch_ledger), name='get_batch_ledger'),
]
