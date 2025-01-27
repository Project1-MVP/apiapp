from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from core.enums.global_enums import Salutation

class CustomerBase(BaseModel):
    name: str
    salutation: Optional[Salutation] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    whatsapp_number: Optional[str] = None
    country: Optional[str] = "IN"
    city: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerResponse(CustomerBase):
    id: UUID
    created_at: int
    updated_at: int

    class Config:
        from_attributes = True
