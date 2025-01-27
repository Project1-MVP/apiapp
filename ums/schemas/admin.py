from pydantic import BaseModel, EmailStr
from typing import Optional, List

class TenantResponse(BaseModel):
    id: int
    business_name: str
    phone_number: str
    email: EmailStr
    is_compliant: bool
    created_at: int
    updated_at: int

    class Config:
        from_attributes = True

class TenantUpdate(BaseModel):
    business_name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    is_compliant: Optional[bool] = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    phone_number: str
    role: str
    is_active: bool
    created_at: int
    updated_at: int

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
