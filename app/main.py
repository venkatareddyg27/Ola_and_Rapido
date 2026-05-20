
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import engine, Base

# MODELS
from app.models.users import *
from app.models.vehicles import *
from app.models.trips import *
from app.models.rentals import *
from app.models.payments import *
from app.models.support import *
from app.models.operations import *


# ROUTERS
from app.routers.auth import router as auth_router
from app.routers import admin as admin_router
from app.routers import trips as trips_router
from app.routers import ratings as ratings_router
from app.routers import rentals as rentals_router
from app.routers import parcels as parcels_router
from app.routers import promo as promo_router
from app.routers import notifications as notifications_router
from app.routers import vehicles as vehicles_router
from app.routers import dispute as dispute_router
from app.routers import drivers as drivers_router
from app.routers import payments as payments_router



# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="Rapido & Ola Backend",

    version="1.0.0",
    
)

version="1.0.0"
app.include_router(auth_router)
app.include_router(admin_router.router)
app.include_router(trips_router.router)
app.include_router(ratings_router.router)
app.include_router(parcels_router.router)
app.include_router(promo_router.router)
app.include_router(notifications_router.router)
app.include_router(vehicles_router.router)
app.include_router(dispute_router.router)
app.include_router(drivers_router.router)
app.include_router(payments_router.router)
app.include_router(rentals_router.router)



# =========================================================
# INCLUDE ROUTERS
# =========================================================

app.include_router(auth_router)


# =========================================================
# ROOT API
# =========================================================

@app.get("/")
async def root():

    return {
        "message": "Backend Running Successfully"
    }