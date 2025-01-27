import time
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
import uuid
from core.database import Base

class TenantBaseModel(Base):
    __abstract__ = True
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(Integer, default=lambda: int(time.time()))
    updated_at = Column(Integer, default=lambda: int(time.time()), onupdate=lambda: int(time.time()))
    
    @declared_attr
    def tenant_id(cls):
        return Column(UUID(as_uuid=True), ForeignKey("tenants.id"), index=True)
        
    @declared_attr 
    def user_id(cls):
        return Column(UUID(as_uuid=True), ForeignKey("users.id"))
