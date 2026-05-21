from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import (
    engine,
    Base
)

# =========================================================
# IMPORT MODELS
# =========================================================

from app.models import *

# =========================================================
# DB CREATE
# =========================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    async with engine.begin() as conn:

        await conn.run_sync(Base.metadata.create_all)

    yield

# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="Rapido & Ola Backend",
    version="1.0.0",
    lifespan=lifespan
)

# =========================================================
# IMPORT ROUTERS
# =========================================================

from app.routers.auth import router as auth_router,profile_router
from app.routers.admin import router as admin_router
from app.routers.trips import router as trips_router
from app.routers.ratings import router as ratings_router
from app.routers.rentals import router as rentals_router
from app.routers.customer_parcels import router as parcels_router
from app.routers.promo import router as promo_router
from app.routers.notifications import router as notifications_router
from app.routers.vehicles import router as vehicles_router
from app.routers.dispute import router as dispute_router
from app.routers.drivers import router as drivers_router
from app.routers.payments import router as payments_router

# =========================================================
# INCLUDE ROUTERS
# =========================================================

app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(admin_router)
app.include_router(trips_router)
app.include_router(ratings_router)
app.include_router(rentals_router)
app.include_router(parcels_router)
app.include_router(promo_router)
app.include_router(notifications_router)
app.include_router(vehicles_router)
app.include_router(dispute_router)
app.include_router(drivers_router)
app.include_router(payments_router)

# =========================================================
# ROOT API
# =========================================================

@app.get("/")
async def root():

    return {
        "message": "Backend Running Successfully"
    }