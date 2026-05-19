# =========================================================
# app/main.py
# =========================================================

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import engine, Base


# =========================================================
# IMPORT ALL MODELS
# =========================================================

<<<<<<< HEAD
import app.models.user_models
import app.models.payment_models
import app.models.escrow_models
=======
from app.models.customer_model import (
    CustomerProfile,
    SavedAddress,
    CustomerPreference,
    EmergencyContact,
    FavoriteDriver,
    LoyaltyTransaction
)
>>>>>>> f0c5970 (Changes are added in models/schemas customer_model.py)
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

    yield


# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan
)


# =========================================================
# CORS MIDDLEWARE
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
async def root():

    return {
        "message": f"{settings.APP_NAME} Running Successfully"
    }


# =========================================================
# HEALTH CHECK API
# =========================================================

@app.get("/health")
async def health_check():

    return {
        "status": "success",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION
    }