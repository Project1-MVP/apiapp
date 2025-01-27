from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from oms.models.orders import Orders, OrderItems
from oms.schemas.orders import *
from oms.services.orders import create_sales_order, add_order_item, checkout_order, delete_order_item
from typing import List
from core.auth import get_current_user

router = APIRouter()

@router.post("/sales", response_model=OrderResponse)
async def create_order(
    order_data: OrderCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await create_sales_order(
        db, 
        order_data, 
        tenant_id=current_user.tenant_id, 
        user_id=current_user.id
    )

@router.post("/sales/{order_id}/items", response_model=OrderItemResponse)
async def add_item_to_order(
    order_id: int,
    item_data: OrderItemCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await add_order_item(
        db, 
        order_id, 
        item_data, 
        tenant_id=current_user.tenant_id
    )

@router.delete("/sales/{order_id}/items/{item_id}", response_model=OrderResponse)
async def remove_item_from_order(
    order_id: int,
    item_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await delete_order_item(
        db,
        order_id,
        item_id,
        tenant_id=current_user.tenant_id
    )

@router.get("/sales/{order_id}/items", response_model=List[OrderItemResponse])
async def get_order_items(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    items = await db.execute(
        select(OrderItems).where(
            OrderItems.order_id == order_id,
            OrderItems.tenant_id == current_user.tenant_id
        )
    )
    return items.scalars().all()

@router.post("/sales/{order_id}/checkout", response_model=OrderResponse)
async def process_checkout(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await checkout_order(
        db, 
        order_id, 
        tenant_id=current_user.tenant_id, 
        user_id=current_user.id
    )

@router.get("/sales/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    order = await db.execute(
        select(Orders).where(
            Orders.id == order_id,
            Orders.tenant_id == current_user.tenant_id
        )
    )
    return order.scalar_one_or_none()

@router.get("/sales", response_model=List[OrderResponse])
async def list_orders(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    orders = await db.execute(
        select(Orders).where(
            Orders.tenant_id == current_user.tenant_id
        )
    )
    return orders.scalars().all()
