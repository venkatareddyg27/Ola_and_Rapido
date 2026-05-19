from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import engine, Base

# USERS
from app.models import user_models
# VEHICLES
from app.models import vehicle
# PAYMENTS
from app.models import payment_models
#customers
from app.models import customer_model

# =========================================================
# LIFESPAN
# =========================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    # =====================================================
    # DEBUG REGISTERED TABLES
    # =====================================================

    print(Base.metadata.tables.keys())

    # =====================================================
    # CREATE DATABASE TABLES
    # =====================================================

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

print("Database tables created successfully")


# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# ROOT API
# =========================================================

@app.get("/")
def root():
    return {
        "message": f"{settings.APP_NAME} Running Successfully"
    }


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health_check():
    return {
        "status": "success",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION
    }