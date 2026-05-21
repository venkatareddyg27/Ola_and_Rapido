from uuid import UUID
from datetime import datetime
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.enums import DriverStatus
from app.models.user_models import DriverProfile, DriverLocation
from app.schemas.user_schemas import (
    DriverLocationCreate,
    DriverProfileResponse,
)

router = APIRouter(prefix="/drivers", tags=["Drivers"])


@router.put("/status")
async def update_driver_status(
    driver_id: UUID,
    status: DriverStatus,
    latitude: Decimal,
    longitude: Decimal,
    heading: Decimal | None = None,
    speed: Decimal | None = None,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(DriverProfile).where(DriverProfile.id == driver_id)
    )
    driver = result.scalar_one_or_none()

    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")

    driver.status = status

    location = DriverLocation(
        driver_id=driver_id,
        latitude=latitude,
        longitude=longitude,
        heading=heading,
        speed=speed,
        is_active=True,
    )

    db.add(location)
    await db.commit()
    await db.refresh(driver)

    return {
        "message": "Driver status and location updated successfully",
        "driver_id": driver.id,
        "status": driver.status,
        "latitude": latitude,
        "longitude": longitude,
    }


@router.get("/performance")
async def get_driver_performance(
    driver_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(DriverProfile).where(DriverProfile.id == driver_id)
    )
    driver = result.scalar_one_or_none()

    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")

    return {
        "driver_id": driver.id,
        "rating": driver.rating,
        "total_trips": driver.total_trips,
        "status": driver.status,
        "subscription_plan": driver.subscription_plan,
        "commission_rate": driver.commission_rate,
    }


@router.get("/locations")
async def get_driver_locations(
    driver_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(DriverLocation)
        .where(DriverLocation.driver_id == driver_id)
        .order_by(DriverLocation.created_at.desc())
    )

    return result.scalars().all()