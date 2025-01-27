from sqlalchemy import Column, String, Float, Integer, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from core.models.base import TenantBaseModel
from core.enums.global_enums import OrderTypeEnum, OrderStatusEnum, PaymentTypeEnum

class OrderItems(TenantBaseModel):
    __tablename__ = "order_items"
    
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"))
    product_batch_id = Column(UUID(as_uuid=True), ForeignKey("product_batches.id"))
    rate = Column(Float)
    quantity = Column(Float)
    discount_percentage = Column(Float, default=0.0)
    Tax = Column(Float)
    MarketingCampain_Discount_return_adjustment = Column(Float, default=0.0)
    amount = Column(Float)
    status = Column(Enum(OrderStatusEnum), default=OrderStatusEnum.PROVISIONING)

class Orders(TenantBaseModel):
    __tablename__ = "orders"
    
    crm_id = Column(UUID(as_uuid=True), ForeignKey("customer.id"), nullable=True)
    order_type = Column(Enum(OrderTypeEnum))
    order_status = Column(Enum(OrderStatusEnum), default=OrderStatusEnum.PROVISIONING)
    sub_total = Column(Float)
    Tax = Column(Float)
    Discount = Column(Float)
    MarketingCampain_Discount = Column(Float)
    Other_Charges = Column(Float)
    Total = Column(Float)
    payment_type = Column(Enum(PaymentTypeEnum))
    related_order_id = Column(UUID(as_uuid=True), ForeignKey("order_items.id"), nullable=True)


