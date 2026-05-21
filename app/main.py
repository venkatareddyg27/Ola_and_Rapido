from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import engine, Base


#endpoints
from app.routers import profile,mobile,login


# =========================================================
# IMPORT ALL MODELS
# =========================================================

import app.models.user_models

import app.models.parcel_models
import app.models.operations
import app.models.vehicle_models
import app.models.base
import app.models.rentals
import app.models.ride_models

# =========================================================
# LIFESPAN
# =========================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("Database tables created successfully")

    yield

# =========================================================
#endpoints
# =========================================================
from app.routers import profile,mobile,login

# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="Ola and Rapido Backend API",
    version="1.0.0",
    lifespan=lifespan,
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
# INCLUDE ROUTERS
# =========================================================
app.include_router(login.router)
app.include_router(mobile.router)
app.include_router(profile.router)