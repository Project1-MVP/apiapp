from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.database import get_db
from core.auth import get_current_user
from typing import List
from ums.models.users import User, Tenant
from ums.schemas.admin import TenantResponse, TenantUpdate, UserResponse, UserUpdate

router = APIRouter()

def check_super_admin(current_user = Depends(get_current_user)):
    if current_user.role != "superadmin":
        raise HTTPException(status_code=403, detail="Only superadmin can access this endpoint")
    return current_user

@router.get("/tenants", response_model=List[TenantResponse])
async def get_all_tenants(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(check_super_admin)
):
    result = await db.execute(select(Tenant))
    return result.scalars().all()

@router.get("/tenants/{tenant_id}/users", response_model=List[UserResponse])
async def get_tenant_users(
    tenant_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(check_super_admin)
):
    result = await db.execute(
        select(User).where(User.tenant_id == tenant_id)
    )
    return result.scalars().all()

@router.put("/tenants/{tenant_id}")
async def update_tenant(
    tenant_id: int,
    tenant_data: TenantUpdate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(check_super_admin)
):
    tenant = await db.execute(
        select(Tenant).where(Tenant.id == tenant_id)
    )
    tenant = tenant.scalar_one_or_none()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    for key, value in tenant_data.dict(exclude_unset=True).items():
        setattr(tenant, key, value)
    
    await db.commit()
    return {"message": "Tenant updated successfully"}

@router.delete("/tenants/{tenant_id}")
async def delete_tenant(
    tenant_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(check_super_admin)
):
    tenant = await db.execute(
        select(Tenant).where(Tenant.id == tenant_id)
    )
    tenant = tenant.scalar_one_or_none()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    await db.delete(tenant)
    await db.commit()
    return {"message": "Tenant deleted successfully"}

@router.put("/users/{user_id}")
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(check_super_admin)
):
    user = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = user.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    for key, value in user_data.dict(exclude_unset=True).items():
        setattr(user, key, value)
    
    await db.commit()
    return {"message": "User updated successfully"}

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(check_super_admin)
):
    user = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = user.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    await db.delete(user)
    await db.commit()
    return {"message": "User deleted successfully"}
