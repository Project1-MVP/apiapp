from datetime import date
from pydantic import BaseModel
from typing import List, Optional
from core.enums.global_enums import OrderTypeEnum, MeasurementUnitsEnum, QRCodeType
from uuid import UUID

class VendorBase(BaseModel):
    vendor_name: str
    contact_person: str
    phone_numbers: List[str]
    email_addresses: List[str]
    gstn: str
    net_term_period: int

class VendorCreate(VendorBase):
    pass

class VendorResponse(VendorBase):
    created_at: int
    updated_at: int

    class Config:
        from_attributes = True
        exclude = {'tenant_id', 'user_id'}

class ProductBase(BaseModel):
    product_name: str
    product_description: str
    product_package: str
    movement_type: OrderTypeEnum
    measurement_unit: MeasurementUnitsEnum
    pid: str

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    created_at: int
    updated_at: int

    class Config:
        from_attributes = True
        exclude = {'tenant_id', 'user_id'}

class ProductBatchBase(BaseModel):
    product_id: int
    vendor_id: int
    rate: float
    csgst_percentage: Optional[float]
    sgst_percentage: Optional[float]
    igst_percentage: Optional[float]
    cess_percentage: Optional[float]
    othertax_percentage: Optional[float]
    cost_price: Optional[float]
    discount: Optional[float]
    marketing_campaign: Optional[dict]
    manufacturing_date: date
    expiry_date: Optional[date]
    batch_id: Optional[str]
    QRcode_type: QRCodeType
    QRcode: Optional[str]
    sku_id: Optional[str]

class ProductBatchCreate(ProductBatchBase):
    pass

class ProductBatchResponse(ProductBatchBase):
    created_at: int
    updated_at: int

    class Config:
        from_attributes = True
        exclude = {'tenant_id', 'user_id'}

class ProductBatchCountResponse(BaseModel):
    id: int
    batch_id: str
    current_stock: float
    created_at: int
    updated_at: int

    class Config:
        from_attributes = True
        exclude = {'tenant_id', 'user_id'}

class ProductBatchLogBookResponse(BaseModel):
    order_id: UUID
    order_type: OrderTypeEnum
    product_batch_id: UUID
    quantity: float
    created_at: int

    class Config:
        from_attributes = True
        exclude = {'tenant_id', 'user_id'}
