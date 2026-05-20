from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.core.database import engine, Base

# IMPORT ALL MODELS

from app.models.users import *
from app.models.vehicles import *
from app.models.trips import *
from app.models.rentals import *
from app.models.payments import *
from app.models.support import *
from app.models.operations import *


# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="Rapido & Ola Backend",
    version="1.0.0"
)


# =========================================================
# ROOT API
# =========================================================

@app.get("/")
async def root():
    return {
        "message": "Backend Running Successfully"
    }