from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.core.enums import UserRole, ServiceType, TripStatus, ParcelStatus
from app.models.user_models import User
from app.models.trips import Trip, TripParcel, TripLocation


router = APIRouter(prefix="/driver/parcels", tags=["Driver Parcels"])


def ensure_driver(current_user: User):
    if current_user.role != UserRole.DRIVER:
        raise HTTPException(
            status_code=403,
            detail="Only drivers can access parcel delivery",
        )


@router.get("/available")
async def available_parcels(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ensure_driver(current_user)

    result = await db.execute(
        select(TripParcel, Trip)
        .join(Trip, Trip.id == TripParcel.trip_id)
        .where(
            Trip.service_type == ServiceType.PARCEL,
            Trip.status == TripStatus.SEARCHING_DRIVER,
            Trip.driver_id.is_(None),
        )
        .order_by(desc(Trip.created_at))
    )

    rows = result.all()

    return [
        {
            "trip_id": trip.id,
            "parcel_id": parcel.id,
            "pickup_address": trip.pickup_address,
            "delivery_address": trip.drop_address,
            "receiver_name": parcel.receiver_name,
            "receiver_phone": parcel.receiver_phone,
            "receiver_address": parcel.receiver_address,
            "package_type": parcel.package_type,
            "weight_kg": parcel.weight_kg,
            "fare": trip.fare,
            "estimated_distance": trip.estimated_distance,
            "vehicle_category": trip.vehicle_category,
            "trip_status": trip.status,
            "parcel_status": parcel.status,
            "created_at": trip.created_at,
        }
        for parcel, trip in rows
    ]


@router.post("/{parcel_id}/accept")
async def accept_parcel(
    parcel_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ensure_driver(current_user)

    result = await db.execute(
        select(TripParcel, Trip)
        .join(Trip, Trip.id == TripParcel.trip_id)
        .where(
            TripParcel.id == parcel_id,
            Trip.service_type == ServiceType.PARCEL,
        )
    )

    row = result.first()

    if not row:
        raise HTTPException(status_code=404, detail="Parcel not found")

    parcel, trip = row

    if trip.driver_id is not None:
        raise HTTPException(status_code=409, detail="Parcel already accepted by another driver")

    if trip.status != TripStatus.SEARCHING_DRIVER:
        raise HTTPException(status_code=400, detail="Parcel is not available for acceptance")

    trip.driver_id = current_user.id
    trip.status = TripStatus.DRIVER_ASSIGNED
    parcel.status = ParcelStatus.DRIVER_ASSIGNED.value
    trip.updated_at = datetime.utcnow()
    parcel.updated_at = datetime.utcnow()

    await db.commit()

    return {
        "message": "Parcel accepted successfully",
        "trip_id": trip.id,
        "parcel_id": parcel.id,
        "trip_status": trip.status,
        "parcel_status": parcel.status,
    }


@router.get("/active")
async def active_driver_parcel(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ensure_driver(current_user)

    result = await db.execute(
        select(TripParcel, Trip)
        .join(Trip, Trip.id == TripParcel.trip_id)
        .where(
            Trip.driver_id == current_user.id,
            Trip.service_type == ServiceType.PARCEL,
            Trip.status.in_(
                [
                    TripStatus.DRIVER_ASSIGNED,
                    TripStatus.DRIVER_ARRIVED,
                    TripStatus.IN_PROGRESS,
                ]
            ),
        )
        .order_by(desc(Trip.created_at))
    )

    row = result.first()

    if not row:
        return {"message": "No active parcel delivery", "data": None}

    parcel, trip = row

    return {
        "trip_id": trip.id,
        "parcel_id": parcel.id,
        "pickup_address": trip.pickup_address,
        "delivery_address": trip.drop_address,
        "receiver_name": parcel.receiver_name,
        "receiver_phone": parcel.receiver_phone,
        "receiver_address": parcel.receiver_address,
        "package_type": parcel.package_type,
        "weight_kg": parcel.weight_kg,
        "fare": trip.fare,
        "estimated_distance": trip.estimated_distance,
        "trip_status": trip.status,
        "parcel_status": parcel.status,
    }


@router.post("/{parcel_id}/arrived-pickup")
async def mark_arrived_pickup(
    parcel_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ensure_driver(current_user)

    row = await get_driver_parcel_row(parcel_id, db, current_user)

    parcel, trip = row

    if trip.status != TripStatus.DRIVER_ASSIGNED:
        raise HTTPException(status_code=400, detail="Driver is not assigned or already moved ahead")

    trip.status = TripStatus.DRIVER_ARRIVED
    parcel.status = ParcelStatus.PICKUP_STARTED.value
    trip.updated_at = datetime.utcnow()
    parcel.updated_at = datetime.utcnow()

    await db.commit()

    return {
        "message": "Driver arrived at pickup location",
        "trip_status": trip.status,
        "parcel_status": parcel.status,
    }


@router.post("/{parcel_id}/pickup")
async def pickup_parcel(
    parcel_id: UUID,
    pod_otp: str = Query(..., min_length=6, max_length=6),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ensure_driver(current_user)

    row = await get_driver_parcel_row(parcel_id, db, current_user)

    parcel, trip = row

    if trip.status != TripStatus.DRIVER_ARRIVED:
        raise HTTPException(status_code=400, detail="Driver must arrive before pickup")

    if parcel.pod_otp != pod_otp:
        raise HTTPException(status_code=400, detail="Invalid pickup OTP")

    trip.status = TripStatus.IN_PROGRESS
    parcel.status = ParcelStatus.PICKED_UP.value
    trip.started_at = datetime.utcnow()
    trip.updated_at = datetime.utcnow()
    parcel.updated_at = datetime.utcnow()

    await db.commit()

    return {
        "message": "Parcel picked up successfully",
        "trip_status": trip.status,
        "parcel_status": parcel.status,
    }


@router.post("/{parcel_id}/deliver")
async def deliver_parcel(
    parcel_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ensure_driver(current_user)

    row = await get_driver_parcel_row(parcel_id, db, current_user)

    parcel, trip = row

    if trip.status != TripStatus.IN_PROGRESS:
        raise HTTPException(status_code=400, detail="Parcel is not in progress")

    trip.status = TripStatus.COMPLETED
    parcel.status = ParcelStatus.DELIVERED.value
    trip.completed_at = datetime.utcnow()
    trip.updated_at = datetime.utcnow()
    parcel.updated_at = datetime.utcnow()

    await db.commit()

    return {
        "message": "Parcel delivered successfully",
        "trip_id": trip.id,
        "parcel_id": parcel.id,
        "trip_status": trip.status,
        "parcel_status": parcel.status,
    }


@router.post("/{parcel_id}/location")
async def update_parcel_location(
    parcel_id: UUID,
    lat: float = Query(...),
    lng: float = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ensure_driver(current_user)

    row = await get_driver_parcel_row(parcel_id, db, current_user)

    parcel, trip = row

    if trip.status not in [
        TripStatus.DRIVER_ASSIGNED,
        TripStatus.DRIVER_ARRIVED,
        TripStatus.IN_PROGRESS,
    ]:
        raise HTTPException(status_code=400, detail="Cannot update location for inactive parcel")

    location = TripLocation(
        trip_id=trip.id,
        lat=lat,
        lng=lng,
    )

    db.add(location)
    await db.commit()

    return {
        "message": "Location updated successfully",
        "trip_id": trip.id,
        "parcel_id": parcel.id,
        "lat": lat,
        "lng": lng,
    }


@router.get("/history/list")
async def driver_parcel_history(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ensure_driver(current_user)

    result = await db.execute(
        select(TripParcel, Trip)
        .join(Trip, Trip.id == TripParcel.trip_id)
        .where(
            Trip.driver_id == current_user.id,
            Trip.service_type == ServiceType.PARCEL,
        )
        .order_by(desc(Trip.created_at))
    )

    rows = result.all()

    return [
        {
            "trip_id": trip.id,
            "parcel_id": parcel.id,
            "pickup_address": trip.pickup_address,
            "delivery_address": trip.drop_address,
            "receiver_name": parcel.receiver_name,
            "receiver_phone": parcel.receiver_phone,
            "fare": trip.fare,
            "estimated_distance": trip.estimated_distance,
            "trip_status": trip.status,
            "parcel_status": parcel.status,
            "created_at": trip.created_at,
            "completed_at": trip.completed_at,
        }
        for parcel, trip in rows
    ]


async def get_driver_parcel_row(
    parcel_id: UUID,
    db: AsyncSession,
    current_user: User,
):
    result = await db.execute(
        select(TripParcel, Trip)
        .join(Trip, Trip.id == TripParcel.trip_id)
        .where(
            TripParcel.id == parcel_id,
            Trip.driver_id == current_user.id,
            Trip.service_type == ServiceType.PARCEL,
        )
    )

    row = result.first()

    if not row:
        raise HTTPException(status_code=404, detail="Parcel not found for this driver")

    return row