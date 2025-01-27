from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from core.database import Base
from core.models.base import TenantBaseModel

class Tenant(Base):
    __tablename__ = "tenants"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_name = Column(String, unique=True, index=True)
    phone_number = Column(String)
    email = Column(String)
    is_complient = Column(Boolean, default=True)

class User(TenantBaseModel):
    __tablename__ = "users"
    
    username = Column(String, unique=True)
    hashed_password = Column(String)
    totp_secret = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    email = Column(String, nullable=True)
    role = Column(String)  # Added role column
    is_active = Column(Boolean, default=True)
