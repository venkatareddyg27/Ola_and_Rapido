from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy import (
    select
)

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.core.database import get_db

from app.models.user_models import (
    DriverProfile
)

router = APIRouter(
    prefix="/admin/drivers",
    tags=["Admin Drivers"]
)

# =========================================================
# GET ALL DRIVERS
# =========================================================

@router.get("/")
async def get_all_drivers(

    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(DriverProfile)
    )

    return result.scalars().all()

# =========================================================
# GET SINGLE DRIVER
# =========================================================

@router.get("/{driver_id}")
async def get_driver(

    driver_id: UUID,

    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(

        select(DriverProfile).where(
            DriverProfile.id == driver_id
        )
    )

    driver = result.scalar_one_or_none()

    if not driver:

        raise HTTPException(
            status_code=404,
            detail="Driver not found"
        )

    return driver

# =========================================================
# VERIFY DRIVER
# =========================================================

@router.put("/{driver_id}/verify")
async def verify_driver(

    driver_id: UUID,

    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(

        select(DriverProfile).where(
            DriverProfile.id == driver_id
        )
    )

    driver = result.scalar_one_or_none()

    if not driver:

        raise HTTPException(
            status_code=404,
            detail="Driver not found"
        )

    driver.is_verified = True

    await db.commit()

    return {
        "message":
        "Driver verified successfully"
    }

# =========================================================
# REJECT DRIVER
# =========================================================

@router.put("/{driver_id}/reject")
async def reject_driver(

    driver_id: UUID,

    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(

        select(DriverProfile).where(
            DriverProfile.id == driver_id
        )
    )

    driver = result.scalar_one_or_none()

    if not driver:

        raise HTTPException(
            status_code=404,
            detail="Driver not found"
        )

    driver.is_verified = False

    await db.commit()

    return {
        "message":
        "Driver rejected"
    }

# =========================================================
# BLOCK DRIVER
# =========================================================

@router.put("/{driver_id}/block")
async def block_driver(

    driver_id: UUID,

    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(

        select(DriverProfile).where(
            DriverProfile.id == driver_id
        )
    )

    driver = result.scalar_one_or_none()

    if not driver:

        raise HTTPException(
            status_code=404,
            detail="Driver not found"
        )

    driver.status = "blocked"

    await db.commit()

    return {
        "message":
        "Driver blocked"
    }