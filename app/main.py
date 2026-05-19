from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import engine, Base


# =========================================================
# IMPORT ALL MODELS
# =========================================================

import app.models.user_models
import app.models.customer_model
import app.models.escrow_models
import app.models.payment_models
import app.models.vehicle
import app.models.driver

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

    #print("Database tables created successfully")

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
async def root():

    return {
        "message": f"{settings.APP_NAME} Running Successfully"
    }


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
async def health_check():

    return {
        "status": "success",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION
    }