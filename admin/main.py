from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from core.middleware.rls import RLSMiddleware
from admin.routes import admin
from core.database import engine, Base

app = FastAPI(title="Multi-tenant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RLSMiddleware)

# Include routers
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
