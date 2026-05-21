from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import engine, Base

# Routers
from app.routers import profile, mobile, login

# Import all models before create_all
import app.models.user_models
import app.models.vehicle_models
import app.models.parcel_models
import app.models.operations
import app.models.rentals
import app.models.ride_models
import app.models.trips


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("Database tables created successfully")

    yield


app = FastAPI(
    title="Ola and Rapido Backend API",
    version="1.0.0",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(login.router)
app.include_router(mobile.router)
app.include_router(profile.router)