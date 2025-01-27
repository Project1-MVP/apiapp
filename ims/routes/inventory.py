import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from core.database import get_db
from core.auth import get_current_user
from typing import List
from ims.schemas.inventory import *
from ims.models.inventory import *

router = APIRouter()

@router.post("/vendors/", response_model=VendorResponse)
async def create_vendor(
    vendor: VendorCreate, 
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_vendor = Vendor(**vendor.dict(), tenant_id=current_user.tenant_id, user_id=current_user.id)
    db.add(db_vendor)
    await db.commit()
    await db.refresh(db_vendor)
    return db_vendor

@router.get("/vendors/", response_model=List[VendorResponse])
async def get_vendors(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    result = await db.execute(
        select(Vendor).where(Vendor.tenant_id == current_user.tenant_id)
    )
    return result.scalars().all()

@router.post("/products/", response_model=ProductResponse)
async def create_product(
    product: ProductCreate, 
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        db_product = Product(**product.dict(), tenant_id=current_user.tenant_id, user_id=current_user.id)
        db.add(db_product)
        await db.commit()
        await db.refresh(db_product)
        return db_product
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=409,
            detail=f"Product with pid {product.pid} already exists"
        )

@router.get("/products/", response_model=List[ProductResponse])
async def get_products(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    result = await db.execute(
        select(Product).where(Product.tenant_id == current_user.tenant_id)
    )
    return result.scalars().all()

@router.post("/product-batches/", response_model=ProductBatchResponse)
async def create_product_batch(
    batch: ProductBatchCreate, 
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Get product details
    product = await db.execute(
        select(Product).where(
            Product.id == batch.product_id,
            Product.tenant_id == current_user.tenant_id
        )
    )
    product = product.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Generate batch_id if not provided
    if not batch.batch_id:
        latest_batch = await db.execute(
            select(ProductBatch)
            .where(ProductBatch.product_id == batch.product_id)
            .order_by(ProductBatch.id.desc())
        )
        latest_batch = latest_batch.scalar_one_or_none()
        
        if latest_batch and latest_batch.batch_id:
            last_seq = int(latest_batch.batch_id[-3:])
            new_seq = str(last_seq + 1).zfill(3)
        else:
            new_seq = "001"
        
        batch.batch_id = f"{product.pid}{new_seq}"

    # Handle QR code generation
    if batch.QRcode_type == QRCodeType.INTERNAL_UPIC:
        batch.QRcode = json.dumps({
            "pid": product.pid,
            "batch": batch.batch_id
        })
    elif not batch.QRcode:
        raise HTTPException(status_code=400, detail="QRcode is required")

    # Create batch
    db_batch = ProductBatch(
        **batch.dict(),
        tenant_id=current_user.tenant_id,
        user_id=current_user.id
    )
    db.add(db_batch)
    await db.commit()
    await db.refresh(db_batch)
    return db_batch

@router.get("/product-batches/count/{batch_id}", response_model=ProductBatchCountResponse)
async def get_batch_count(
    batch_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    result = await db.execute(
        select(ProductBatchCount).where(
            ProductBatchCount.product_batch_id == batch_id,
            ProductBatchCount.tenant_id == current_user.tenant_id
        )
    )
    count = result.scalar_one_or_none()
    if not count:
        raise HTTPException(status_code=404, detail="Batch count not found")
    return count

@router.get("/product-batches/audit/{batch_id}", response_model=List[ProductBatchLogBookResponse])
async def get_batch_audit(
    batch_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    result = await db.execute(
        select(ProductBatchLogBook)
        .where(
            ProductBatchLogBook.product_batch_id == batch_id,
            ProductBatchLogBook.tenant_id == current_user.tenant_id
        )
        .order_by(ProductBatchLogBook.timestamp.desc())
    )
    return result.scalars().all()

@router.get("/product/getItem/{pid}", response_model=List[ProductBatchResponse])
async def get_available_product_batches(
    pid: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Get product by pid
    product = await db.execute(
        select(Product).where(
            Product.pid == pid,
            Product.tenant_id == current_user.tenant_id
        )
    )
    product = product.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Get product batches with available quantity
    result = await db.execute(
        select(ProductBatch, ProductBatchCount)
        .join(ProductBatchCount, ProductBatch.id == ProductBatchCount.product_batch_id)
        .where(
            ProductBatch.product_id == product.id,
            ProductBatch.tenant_id == current_user.tenant_id,
            ProductBatchCount.current_stock > 0
        )
    )
    
    available_batches = result.scalars().all()
    
    if not available_batches:
        raise HTTPException(
            status_code=404,
            detail="No Product Batches has required quantity"
        )
    
    return available_batches

@router.get("/product-batch/getItem/{QRcode}", response_model=ProductBatchResponse)
async def get_product_batch_by_qr(
    QRcode: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Get product batch by QRcode
    result = await db.execute(
        select(ProductBatch).where(
            ProductBatch.QRcode == QRcode,
            ProductBatch.tenant_id == current_user.tenant_id
        )
    )
    
    batch = result.scalar_one_or_none()
    if not batch:
        raise HTTPException(
            status_code=404,
            detail="Product Batch not found for given QR code"
        )
    
    return batch