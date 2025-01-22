from core.database import get_db


@router.get("/inventory")
async def get_inventory():
    conn = await get_db().__anext__()
    results = await conn.fetch("SELECT * FROM inventory WHERE tenant_id = current_setting('tenant_id')::integer")
    return results
