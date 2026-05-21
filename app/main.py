from fastapi import FastAPI

from app.core.database import (
    engine,
    Base
)

# =========================================================
# IMPORT MODELS
# =========================================================

from app.models.user_models import *
from app.models.vehicles import *
from app.models.trips import *
from app.models.rentals import *
from app.models.payments import *
from app.models.support import *
from app.models.operations import *

# =========================================================
# IMPORT ROUTERS
# =========================================================

from app.routers.auth import (
    router as auth_router
)

from app.routers.admin import (
    router as admin_router
)

from app.routers.trips import (
    router as trips_router
)

from app.routers.ratings import (
    router as ratings_router
)

from app.routers.rentals import (
    router as rentals_router
)

from app.routers.parcels import (
    router as parcels_router
)

from app.routers.promo import (
    router as promo_router
)

from app.routers.notifications import (
    router as notifications_router
)

from app.routers.vehicles import (
    router as vehicles_router
)

from app.routers.dispute import (
    router as dispute_router
)

from app.routers.drivers import (
    router as drivers_router
)

from app.routers.payments import (
    router as payments_router
)

# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="Rapido & Ola Backend",
    version="1.0.0"
)

# =========================================================
# INCLUDE ROUTERS
# =========================================================

app.include_router(auth_router)

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
        "message":
        "Backend Running Successfully"
    }