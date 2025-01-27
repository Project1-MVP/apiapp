from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from aams.schemas.SignIn import *
from aams.services.SignIn import AuthService
from ums.models.users import User, Tenant

router = APIRouter()

@router.post("/register/tenant", response_model=dict)
async def register_tenant(
    tenant_data: TenantRegistration,
    db: AsyncSession = Depends(get_db)
):
    # Create tenant
    tenant = Tenant(
        business_name=tenant_data.business_name,
        phone_number=tenant_data.phone_number,
        email=tenant_data.email
    )
    db.add(tenant)
    await db.flush()
    
    # Create admin user
    totp_secret = AuthService.create_totp_secret()
    user = User(
        tenant_id=tenant.id,
        username=tenant_data.username,
        hashed_password=AuthService.get_password_hash(tenant_data.password),
        totp_secret=totp_secret,
        role="admin"
    )
    db.add(user)
    await db.commit()
    
    return {
        "message": "Tenant registered successfully",
        "totp_url": AuthService.get_totp_provisioning_url(tenant_data.username, totp_secret)
    }

@router.post("/register/user", response_model=dict)
async def register_user(
    user_data: UserRegistration,
    db: AsyncSession = Depends(get_db)
):
    totp_secret = AuthService.create_totp_secret()
    user = User(
        username=user_data.username,
        hashed_password=AuthService.get_password_hash(user_data.password),
        totp_secret=totp_secret,
        phone_number=user_data.phone_number,
        email=user_data.email,
        role=user_data.role
    )
    db.add(user)
    await db.commit()
    
    return {
        "message": "User registered successfully",
        "totp_url": AuthService.get_totp_provisioning_url(user_data.username, totp_secret)
    }

@router.post("/verify-totp")
async def verify_totp(
    verification: TOTPVerification,
    db: AsyncSession = Depends(get_db)
):
    user = await db.query(User).filter(User.username == verification.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    if AuthService.verify_totp(user.totp_secret, verification.totp_code):
        user.is_active = True
        await db.commit()
        return {"message": "TOTP verified successfully"}
    raise HTTPException(status_code=400, detail="Invalid TOTP code")

@router.post("/login", response_model=TokenResponse)
async def login(
    Login_data: Login,
    db: AsyncSession = Depends(get_db)
):
    user = await db.execute(
        select(User).where(User.username == Login_data.username)
    )
    user = user.scalar_one_or_none()
    
    if not user or not AuthService.verify_password(Login_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not user.is_active:
        raise HTTPException(status_code=401, detail="User not activated")
        
    if not AuthService.verify_totp(user.totp_secret, Login_data.totp_code):
        raise HTTPException(status_code=401, detail="Invalid TOTP code")
        
    token_data = {
        "sub": user.username,
        "tenant_id": str(user.tenant_id),
        "user_id": str(user.id),
        "role": user.role
    }
    return {
        "access_token": AuthService.create_access_token(token_data),
        "token_type": "bearer"
    }

@router.post("/forgot-password")
async def forgot_password(
    reset_data: ForgotPassword,
    db: AsyncSession = Depends(get_db)
):
    user = await db.query(User).filter(User.username == reset_data.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    if AuthService.verify_totp(user.totp_secret, reset_data.totp_code):
        user.hashed_password = AuthService.get_password_hash(reset_data.new_password)
        await db.commit()
        return {"message": "Password reset successfully"}
    raise HTTPException(status_code=400, detail="Invalid TOTP code")

@router.post("/verify-forgotpassword-totp")
async def verify_forgotpassword_totp(
    verification: TOTPVerification,
    db: AsyncSession = Depends(get_db)
):
    user = await db.execute(
        select(User).where(User.username == verification.username)
    )
    user = user.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    if AuthService.verify_totp(user.totp_secret, verification.totp_code):
        user.is_active = True
        await db.commit()
        return {"message": "TOTP verified successfully"}
    raise HTTPException(status_code=400, detail="Invalid TOTP code")
