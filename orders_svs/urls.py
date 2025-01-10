from django.urls import path
from . import views

urlpatterns = [
    path('provision/add-product/', views.add_provision_order_item, name='add-provision-order-item'),
    path('provision/create/', views.create_provision_order_batch, name='create_provision_order'),
    path('provision/product/<uuid:order_id>/update/', views.update_provision_order_item, name='update_product_provision_order'),
    path('provision/product/<uuid:order_id>/delete/', views.delete_provision_order_item, name='delete_product_provision_order'),
    path('provision/<uuid:orderBatch_id>/checkout/', views.checkout_provision_order_batch, name='checkout_provision_order'),
]