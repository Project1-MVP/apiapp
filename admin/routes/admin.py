from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from core.database import execute_transaction
from pydantic import BaseModel
import pyotp
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from core.config import settings

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="admin/token")

class TenantCreate(BaseModel):
    business_name: str
    phone_number: str
    email: str
    username: str
    password: str

@router.post("/register")
async def register_admin(username: str, email: str, password: str):
    await execute_transaction(
        """
        INSERT INTO admins (username, email, hashed_password, totp_secret)
        VALUES ($1, $2, $3, $4)
        """,
        username,
        email,
        pwd_context.hash(password),
        pyotp.random_base32()
    )
    return {"message": "Admin registered successfully"}

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), totp_code: str = None):
    conn = await get_db().__anext__()
    admin = await conn.fetchrow(
        "SELECT * FROM admins WHERE username = $1",
        form_data.username
    )
    if not admin or not pwd_context.verify(form_data.password, admin['hashed_password']):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    totp = pyotp.TOTP(admin['totp_secret'])
    if not totp.verify(totp_code):
        raise HTTPException(status_code=400, detail="Invalid TOTP code")
    
    access_token = create_access_token(data={"sub": admin['username']})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/tenant/register", status_code=status.HTTP_201_CREATED)
async def register_tenant(tenant: TenantCreate):
    try:
        await execute_transaction(
            """
            WITH new_tenant AS (
                INSERT INTO tenants (business_name, phone_number, email)
                VALUES ($1, $2, $3)
                RETURNING id
            )
            INSERT INTO users (tenant_id, username, hashed_password, role)
            VALUES (
                (SELECT id FROM new_tenant),
                $4,
                $5,
                'owner'
            )
            """,
            tenant.business_name,
            tenant.phone_number,
            tenant.email,
            tenant.username,
            pwd_context.hash(tenant.password)
        )
        return {"message": "Tenant registered successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
