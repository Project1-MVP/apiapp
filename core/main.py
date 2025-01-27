from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from core.middleware.rls import RLSMiddleware
from core.database import engine, Base
from core.auth import get_current_user

# Import routers from services
from aams.routes import SignIn
from crs.routes import customer
from ums.routes import admin
from ims.routes import inventory
from oms.routes import orders

#daee
#Digital Assistance for Enterprise Excellence
# Dynamic Applications for Enterprise Empowerment
# Data-Driven Analytics for Enterprise Evolution
# Digital Automation for Economic Enablement
# Driving Advanced Enterprise Efficiency
# Development and Advancement for Enterprise Excellence
# Digital Aid for Emerging Economies
# Delivering AI and Enterprise Efficiency
# Data Analytics and Enterprise Empowerment

from fastapi.security import OAuth2PasswordBearer

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # Create tables
    yield  # Application runs here
    # Shutdown logic (optional, if needed)

# OAuth2 scheme for authentication
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/SignIn/login",  # This should match your login endpoint
)

# FastAPI app initialization
app = FastAPI(
    title="StockIt",
    description="Model StockIt API",
    version="1.0.0",
    lifespan=lifespan,
    openapi_url="/api/openapi.json",  # Custom OpenAPI JSON URL
    swagger_ui_oauth2_redirect_url="/api/SignIn/login",  # Redirect URL for Swagger OAuth2
)

# Add middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RLSMiddleware)

# Public routes
app.include_router(SignIn.router, prefix="/api/SignIn", tags=["SignIn"])

# Protected routes requiring JWT
app.include_router(
    inventory.router, 
    prefix="/api/inventory", 
    tags=["Inventory"],
    dependencies=[Depends(get_current_user)]
)
app.include_router(
    orders.router, 
    prefix="/api/orders", 
    tags=["Orders"],
    dependencies=[Depends(get_current_user)]
)
app.include_router(
    admin.router, 
    prefix="/api/admin", 
    tags=["Admin"],
    dependencies=[Depends(get_current_user)]
)

app.include_router(
    customer.router,
    prefix="/api/customer",
    tags=["Customers"],
    dependencies=[Depends(get_current_user)]
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",  # Replace "main:app" with your module and app name
        host="0.0.0.0",
        port=8000,
        #ssl_certfile="cert.pem",  # Path to your SSL certificate
        #ssl_keyfile="key.pem",    # Path to your SSL private key
        #log_level="info"
    )



