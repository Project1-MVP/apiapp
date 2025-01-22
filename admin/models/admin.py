from sqlalchemy import Column, Integer, String, Boolean
from core.database import Base

class Admin(Base):
    __tablename__ = "admins"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    totp_secret = Column(String)
    is_active = Column(Boolean, default=True)
