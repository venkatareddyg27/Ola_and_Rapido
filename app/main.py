from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import engine, Base


from app.models.users import *
from app.models.vehicles import *
from app.models.trips import *
from app.models.rentals import *
from app.models.payments import *
from app.models.support import *
from app.models.operations import *

from app.routers import trips as trips_router
from app.routers import ratings as ratings_router
from app.routers import parcels as parcels_router
from app.routers import promo as promo_router
from app.routers import notifications as notifications_router

@asynccontextmanager
async def lifespan(app: FastAPI):

    # Create all tables
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

app.include_router(trips_router.router)
app.include_router(ratings_router.router)
app.include_router(parcels_router.router)
app.include_router(promo_router.router)
app.include_router(notifications_router.router)

# =========================================================
# ROOT API
# =========================================================

@app.get("/")
async def root():
    return {
        "message": "Backend Running Successfully"
    }