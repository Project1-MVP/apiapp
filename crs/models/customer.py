from sqlalchemy import Column, String, Enum
from core.models.base import TenantBaseModel
from core.enums.global_enums import Salutation

class Customer(TenantBaseModel):
    __tablename__ = "customer"
    
    name = Column(String, nullable=False)
    salutation =  Column(Enum(Salutation))
    phone_number = Column(String, unique=True)
    email = Column(String)
    whatsapp_number = Column(String)
    country = Column(String, default="IN")
    city = Column(String)
