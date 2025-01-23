from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from core.database import Base

class Tenant(Base):
    __tablename__ = "tenants"
    
    id = Column(Integer, primary_key=True, index=True)
    business_name = Column(String, unique=True, index=True)
    phone_number = Column(String)
    email = Column(String)
    is_complient = Column(Boolean, default=True)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    totp_secret = Column(String)
    phone_number = Column(String)
    email = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="user")
