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

from app.models.payment_models import *
from app.models.escrow_models import *
from app.models.ride_models import *

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
#endpoints
# =========================================================



app.include_router(login.router)
app.include_router(mobile.router)
app.include_router(profile.router)
