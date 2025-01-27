from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from core.auth import get_current_user
from typing import List
from crs.models.customer import Customer
from crs.schemas.customer import *
from crs.services.customer import get_customer_orders
from uuid import UUID

from oms.schemas.orders import OrderResponse

router = APIRouter()

@router.post("/", response_model=CustomerResponse)
async def create_customer(
    customer: CustomerCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_customer = Customer(**customer.dict(), tenant_id=current_user.tenant_id)
    db.add(db_customer)
    await db.commit()
    return db_customer

@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(
    customer_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    customer = await db.execute(
        select(Customer).where(
            Customer.id == customer_id,
            Customer.tenant_id == current_user.tenant_id
        )
    )
    return customer.scalar_one_or_none()

@router.put("/{customer_id}", response_model=CustomerResponse)
async def update_customer(
    customer_id: UUID,
    customer: CustomerCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_customer = await db.execute(
        select(Customer).where(
            Customer.id == customer_id,
            Customer.tenant_id == current_user.tenant_id
        )
    )
    db_customer = db_customer.scalar_one_or_none()
    for key, value in customer.dict(exclude_unset=True).items():
        setattr(db_customer, key, value)
    await db.commit()
    return db_customer

@router.delete("/{customer_id}")
async def delete_customer(
    customer_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_customer = await db.execute(
        select(Customer).where(
            Customer.id == customer_id,
            Customer.tenant_id == current_user.tenant_id
        )
    )
    db_customer = db_customer.scalar_one_or_none()
    await db.delete(db_customer)
    await db.commit()
    return {"message": "Customer deleted"}

@router.get("/orders/{identifier}", response_model=List[OrderResponse])
async def get_customer_orders_by_identifier(
    identifier: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await get_customer_orders(db, identifier)
