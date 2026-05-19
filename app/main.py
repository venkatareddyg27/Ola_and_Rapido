# main.py

from contextlib import asynccontextmanager

from fastapi import FastAPI


from app.core.database import engine, Base
from core.config import settings
from core.database import engine, Base


# =========================================================

# IMPORT ALL MODELS


from app.models.user_model import (
    User,
    DriverProfile,
    KYCDocument,
    OTPLog,
    DriverSubscription,
)

# IMPORT ALL MODELS

from models.users import *
from models.vehicles import *
from models.trips import *
from models.rentals import *
from models.payments import *
from models.support import *
from models.operations import *


# =========================================================
# LIFESPAN
# =========================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    # =====================================================
    # DEBUG REGISTERED TABLES
    # =====================================================

    print("\nRegistered Tables:")
    print(Base.metadata.tables.keys())

    # =====================================================
    # CREATE DATABASE TABLES
    # =====================================================

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("\nDatabase tables created successfully")

    yield


# =========================================================
# FASTAPI APP
# =========================================================


app = FastAPI(
    title="Rapido & Ola Backend",
    version="1.0.0"
)


# =====================================================
# CREATE DATABASE TABLES
# =====================================================

Base.metadata.create_all(bind=engine)


# =====================================================
# ROOT API
# =====================================================

@app.get("/")
async def root():
    return {
        "message": "Backend Running Successfully"
    }