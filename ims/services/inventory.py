from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ims.models.inventory import Product, ProductBatch, ProductBatchCount, ProductBatchLogBook
from ums.models.users import User
from core.enums.global_enums import OrderTypeEnum

async def handle_stock_movement(
    db: AsyncSession,
    order_id: str,
    order_type: OrderTypeEnum,
    product_batch_id: int,
    quantity: float,
    tenant_id: int,
    user_id: int
) -> dict:
    # Verify user belongs to tenant
    user = await db.execute(
        select(User).where(
            User.id == user_id,
            User.tenant_id == tenant_id
        )
    )
    if not user.scalar_one_or_none():
        raise HTTPException(status_code=403, detail="User not authorized for this tenant")

    # Get current stock count
    batch_count = await db.execute(
        select(ProductBatchCount).where(
            ProductBatchCount.product_batch_id == product_batch_id,
            ProductBatchCount.tenant_id == tenant_id
        )
    )
    current_count = batch_count.scalar_one_or_none()
    
    if not current_count:
        raise HTTPException(status_code=404, detail="Product batch not found")

    # Calculate new quantity based on movement type
    if order_type in [OrderTypeEnum.CHECKIN, OrderTypeEnum.RETURN, OrderTypeEnum.PURCHASE]:
        new_quantity = current_count.current_stock + quantity
    else:
        if current_count.current_stock < quantity:
            raise HTTPException(status_code=400, detail="Insufficient stock")
        new_quantity = current_count.current_stock - quantity

    # Update stock count
    current_count.current_stock = new_quantity
    
    # Create audit entry
    audit_entry = ProductBatchLogBook(
        order_id=order_id,
        order_type=order_type,
        product_batch_id=product_batch_id,
        quantity=quantity,
        user_id=user_id,
        tenant_id=tenant_id
    )
    
    db.add(audit_entry)
    await db.commit()

    return {
        "status": "success",
        "new_stock_level": new_quantity,
        "movement_type": order_type,
        "quantity": quantity
    }
