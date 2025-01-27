from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from crs.models.customer import Customer
from oms.models.orders import Orders
from sqlalchemy.dialects.postgresql import UUID

async def get_customer_orders(db: AsyncSession, identifier: str):
    query = select(Orders).join(Customer)
    if isinstance(identifier, UUID):
        query = query.where(Customer.id == identifier)
    else:
        query = query.where(Customer.phone_number == identifier)
    
    result = await db.execute(query)
    return result.scalars().all()