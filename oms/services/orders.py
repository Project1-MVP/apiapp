
import time
from fastapi import HTTPException
from sqlalchemy import UUID, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from oms.models.orders import Orders, OrderItems
from ims.models.inventory import ProductBatch, ProductBatchCount
from ims.services.inventory import handle_stock_movement
from core.enums.global_enums import OrderStatusEnum, OrderTypeEnum
from oms.schemas.orders import OrderItemCreate, OrderItemResponse, OrderCreate, OrderResponse

async def create_sales_order(
    db: AsyncSession,
    order_data: OrderCreate,
    tenant_id: int,
    user_id: int
) -> Orders:
    sales_order = OrderCreate(
        **order_data.dict(),
        tenant_id=tenant_id,
        user_id=user_id,
        order_type=OrderTypeEnum.SALE
    )
    db.add(sales_order)
    await db.commit()
    return sales_order

async def add_order_item(
    db: AsyncSession,
    order_id: int,
    item_data: OrderItemCreate,
    tenant_id: int
) -> OrderResponse:
    # Check order status
    order = await db.execute(
        select(Orders)
        .where(
            Orders.id == order_id,
            Orders.tenant_id == tenant_id,
            Orders.order_status == OrderStatusEnum.PROVISIONING
        )
    )
    order = order.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found or not in PROVISIONING status")

    # Check stock availability
    batch_count = await db.execute(
        select(ProductBatchCount)
        .where(
            ProductBatchCount.product_batch_id == item_data.product_batch_id,
            ProductBatchCount.tenant_id == tenant_id
        )
    )
    batch_count = batch_count.scalar_one_or_none()
    if not batch_count or batch_count.current_stock < item_data.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    # Get product batch details
    product_batch = await db.execute(
        select(ProductBatch)
        .where(ProductBatch.id == item_data.product_batch_id)
    )
    product_batch = product_batch.scalar_one_or_none()

    # Check existing order item
    existing_item = await db.execute(
        select(OrderItems)
        .where(
            OrderItems.order_id == order_id,
            OrderItems.product_batch_id == item_data.product_batch_id
        )
    )
    existing_item = existing_item.scalar_one_or_none()

    price_per_unit = product_batch.mrp * (1 - product_batch.discount/100)
    item_total = price_per_unit * item_data.quantity

    if existing_item:
        existing_item.quantity = item_data.quantity
        existing_item.price = price_per_unit
        order_item = existing_item
    else:
        order_item = OrderItems(
            order_id=order_id,
            product_batch_id=item_data.product_batch_id,
            quantity=item_data.quantity,
            mrp=product_batch.mrp,
            price=price_per_unit,
            tenant_id=tenant_id
        )
        db.add(order_item)

    # Update order totals
    order.total_order_value = item_total
    order.final_price = item_total * (1 - order.pos_discount/100) * (1 - order.marketing_campaign_discount/100)
    
    items = await db.execute(
        select(OrderItems).where(OrderItems.order_id == order_id)
    )
    order.order_items = items.scalars().all()
    
    await db.commit()
    return order

async def delete_order_item(
    db: AsyncSession,
    order_id: int,
    item_id: UUID,
    tenant_id: int
) -> OrderResponse:
    # Delete item
    await db.execute(
        delete(OrderItems).where(
            OrderItems.id == item_id,
            OrderItems.order_id == order_id,
            OrderItems.tenant_id == tenant_id
        )
    )
    
    # Get updated order with remaining items
    order = await db.execute(
        select(Orders).where(Orders.id == order_id)
    )
    order = order.scalar_one_or_none()
    
    items = await db.execute(
        select(OrderItems).where(OrderItems.order_id == order_id)
    )
    order.order_items = items.scalars().all()
    
    # Recalculate order totals
    order.total_order_value = sum(item.price * item.quantity for item in order.order_items)
    order.final_price = order.total_order_value * (1 - order.pos_discount/100) * (1 - order.marketing_campaign_discount/100)
    
    await db.commit()
    return order


async def checkout_order(
    db: AsyncSession,
    order_id: int,
    tenant_id: int,
    user_id: int
) -> Orders:
    # Get order with items
    order = await db.execute(
        select(Orders)
        .where(
            Orders.id == order_id,
            Orders.tenant_id == tenant_id,
            Orders.order_status == OrderStatusEnum.PROVISIONING
        )
    )
    order = order.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found or not in PROVISIONING status")

    # Get order items
    items = await db.execute(
        select(OrderItems)
        .where(OrderItems.order_id == order_id)
    )
    items = items.scalars().all()

    # Recheck stock and update inventory
    for item in items:
        await handle_stock_movement(
            db=db,
            order_id=str(order_id),
            order_type=OrderTypeEnum.SALE,
            product_batch_id=item.product_batch_id,
            quantity=item.quantity,
            tenant_id=tenant_id,
            user_id=user_id
        )
        item.status = OrderStatusEnum.COMPLETED

    # Update order
    order.order_status = OrderStatusEnum.COMPLETED
    
    await db.commit()
    return order

