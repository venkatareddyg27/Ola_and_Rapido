from fastapi import FastAPI

from app.core.database import engine, Base
# IMPORT ALL MODELS

from app.models.user_model import (
    User,
    DriverProfile,
    KYCDocument,
    OTPLog,
    DriverSubscription,
)

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