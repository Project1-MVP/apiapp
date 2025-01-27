from datetime import date
import time
from sqlalchemy import Boolean, Column, String, Float, Date, ARRAY, ForeignKey, Enum, Integer
from sqlalchemy.dialects.postgresql import JSONB
from core.models.base import TenantBaseModel
from core.enums.global_enums import OrderTypeEnum, MeasurementUnitsEnum, QRCodeType
from sqlalchemy.dialects.postgresql import UUID

class Vendor(TenantBaseModel):
    __tablename__ = "vendors"
    vendor_name = Column(String, index=True)
    contact_person = Column(String)
    phone_numbers = Column(ARRAY(String))
    email_addresses = Column(ARRAY(String))
    gstn = Column(String)
    net_term_period = Column(Integer)

class Product(TenantBaseModel):
    __tablename__ = "products"
    product_name = Column(String, index=True)
    product_description = Column(String)
    product_package = Column(String)
    movement_type = Column(Enum(OrderTypeEnum))
    measurement_unit = Column(Enum(MeasurementUnitsEnum))
    pid = Column(String, unique=True)

class ProductBatch(TenantBaseModel):
    __tablename__ = "product_batches"
    product_id = Column(UUID, ForeignKey("products.id"))
    vendor_id = Column(UUID, ForeignKey("vendors.id"), nullable=True)
    rate = Column(Float)
    csgst_percentage = Column(Float, nullable=True)
    sgst_percentage = Column(Float, nullable=True)
    igst_percentage = Column(Float, nullable=True)
    cess_percentage = Column(Float, nullable=True)
    othertax_percentage = Column(Float, nullable=True)
    cost_price = Column(Float, nullable=True)
    discount = Column(Float, nullable=True)
    marketing_campaign = Column(JSONB, nullable=True)
    manufacturing_date = Column(Date, default=lambda: date.today())
    expiry_date = Column(Date, nullable=True)
    batch_id = Column(String)
    QRcode_type = Column(Enum(QRCodeType))
    QRcode = Column(String)
    sku_id = Column(String, nullable=True)

class ProductBatchCount(TenantBaseModel):
    __tablename__ = "product_batch_counts"
    product_batch_id = Column(UUID, ForeignKey("product_batches.id"))
    current_stock = Column(Float)

class ProductBatchLogBook(TenantBaseModel):
    __tablename__ = "product_batch_audits"
    order_id = Column(String)
    order_type = Column(Enum(OrderTypeEnum))
    product_batch_id = Column(UUID, ForeignKey("product_batches.id"))
    quantity = Column(Float)