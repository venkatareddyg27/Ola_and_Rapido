from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import engine, Base

from app.models.vehicle import (
    Vehicle,
    VehicleListing
)

# =========================================================
# CREATE TABLES
# =========================================================

Base.metadata.create_all(bind=engine)

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