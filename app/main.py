
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

# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="Rapido & Ola Backend",
    version="1.0.0",
    
)


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