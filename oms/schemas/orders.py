from pydantic import BaseModel
from uuid import UUID
from core.enums.global_enums import OrderTypeEnum, OrderStatusEnum, PaymentTypeEnum
from typing import List, Optional

class OrderItemCreate(BaseModel):
    product_batch_id: UUID
    quantity: float

class OrderItemResponse(BaseModel):
    id: UUID
    order_id: UUID
    product_batch_id: UUID
    quantity: float
    rate: float
    discount: float
    price: float
    status: OrderStatusEnum
    created_at: int
    updated_at: int
    
    class Config:
        from_attributes = True
        exclude = {'tenant_id', 'user_id'}

class OrderCreate(BaseModel):
    crm_id: str
    phone_number: str
    payment_type: PaymentTypeEnum

class OrderResponse(BaseModel):
    id: UUID
    crm_id: str
    phone_number: str
    order_type: OrderTypeEnum
    order_status: OrderStatusEnum
    sale_at: Optional[int]
    total_order_value: float
    pos_discount: float
    marketing_campaign_discount: float
    final_price: float
    payment_type: PaymentTypeEnum
    created_at: int
    updated_at: int
    order_items: List[OrderItemResponse] = []
    
    class Config:
        from_attributes = True
        exclude = {'tenant_id', 'user_id'}

