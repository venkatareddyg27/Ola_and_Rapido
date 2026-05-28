from uuid import UUID
from decimal import Decimal
from datetime import datetime
import random

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.core.enums import (
    UserRole,
    ServiceType,
    TripStatus,
    ParcelStatus,
    VehicleCategory,
)
from app.models.user_models import User
from app.models.trips import Trip, TripParcel, TripLocation
from app.schemas.parcel import ParcelCreate, ParcelBookingResponse
from app.services.fare import FareCalculatorService
from app.services.distance_service import DistanceService


router = APIRouter(prefix="/customer/parcels", tags=["Customer Parcels"])


def ensure_customer(current_user: User):
    if current_user.role != UserRole.CUSTOMER:
        raise HTTPException(
            status_code=403,
            detail="Only customers can access parcel booking",
        )


def generate_otp() -> str:
    return str(random.randint(100000, 999999))


def select_vehicle_by_weight(weight_kg: float) -> VehicleCategory:
    if weight_kg < 1 or weight_kg > 10:
        raise HTTPException(
            status_code=400,
            detail="Parcel weight must be between 1kg and 10kg",
        )

    if weight_kg <= 4:
        return VehicleCategory.BIKE

    return VehicleCategory.AUTO


@router.post("/parcel_book", response_model=ParcelBookingResponse)
async def book_parcel(
    payload: ParcelCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ensure_customer(current_user)

    distance_km = DistanceService.calculate_distance(
        float(payload.pickup_lat),
        float(payload.pickup_lng),
        float(payload.delivery_lat),
        float(payload.delivery_lng),
    )

    vehicle_category = select_vehicle_by_weight(float(payload.weight_kg))

    fare_data = FareCalculatorService.calculate_delivery_charge(
        distance_km=distance_km,
        weight_kg=payload.weight_kg,
        priority=payload.priority,
    )

    trip = Trip(
        customer_id=current_user.id,
        pickup_address=payload.pickup_address,
        drop_address=payload.delivery_address,
        pickup_lat=payload.pickup_lat,
        pickup_lng=payload.pickup_lng,
        drop_lat=payload.delivery_lat,
        drop_lng=payload.delivery_lng,
        service_type=ServiceType.PARCEL,
        vehicle_category=vehicle_category,
        status=TripStatus.PENDING_CONFIRMATION,
        estimated_distance=Decimal(str(round(distance_km, 2))),
        estimated_fare=Decimal(str(fare_data["total_charge"])),
        fare=Decimal(str(fare_data["total_charge"])),
        ride_otp=generate_otp(),
    )

    db.add(trip)
    await db.flush()

    sender_name = (
        getattr(current_user, "username", None)
        or getattr(current_user, "name", None)
        or getattr(current_user, "full_name", None)
        or "Customer"
    )

    sender_phone = (
        getattr(current_user, "mobile_number", None)
        or getattr(current_user, "phone", None)
        or "0000000000"
    )

    parcel = TripParcel(
        trip_id=trip.id,
        sender_name=sender_name,
        sender_phone=sender_phone,
        receiver_name=payload.receiver_name,
        receiver_phone=payload.receiver_phone,
        receiver_address=payload.receiver_address,
        package_type=payload.package_type,
        weight_kg=payload.weight_kg,
        cod_amount=Decimal("0.00"),
        pod_otp=generate_otp(),
        status=ParcelStatus.PENDING_CONFIRMATION.value,
    )

    db.add(parcel)
    await db.commit()
    await db.refresh(trip)
    await db.refresh(parcel)

    return {
        "message": "Parcel draft created. Please review and confirm.",
        "trip_id": trip.id,
        "parcel_id": parcel.id,
        "distance_km": trip.estimated_distance,
        "delivery_charge": trip.fare,
        "vehicle_category": trip.vehicle_category,
        "trip_status": trip.status,
        "parcel_status": parcel.status,
    }


@router.get("/{parcel_id}/summary")
async def get_parcel_summary(
    parcel_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ensure_customer(current_user)

    result = await db.execute(
        select(TripParcel, Trip)
        .join(Trip, Trip.id == TripParcel.trip_id)
        .where(
            TripParcel.id == parcel_id,
            Trip.customer_id == current_user.id,
            Trip.service_type == ServiceType.PARCEL,
        )
    )

    row = result.first()

    if not row:
        raise HTTPException(status_code=404, detail="Parcel not found")

    parcel, trip = row

    return {
        "parcel_id": parcel.id,
        "trip_id": trip.id,
        "sender_name": parcel.sender_name,
        "sender_phone": parcel.sender_phone,
        "receiver_name": parcel.receiver_name,
        "receiver_phone": parcel.receiver_phone,
        "receiver_address": parcel.receiver_address,
        "pickup_address": trip.pickup_address,
        "delivery_address": trip.drop_address,
        "package_type": parcel.package_type,
        "weight_kg": parcel.weight_kg,
        "distance_km": trip.estimated_distance,
        "delivery_charge": trip.fare,
        "vehicle_category": trip.vehicle_category,
        "trip_status": trip.status,
        "parcel_status": parcel.status,
        "created_at": trip.created_at,
    }


@router.post("/{parcel_id}/confirm")
async def confirm_parcel_booking(
    parcel_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ensure_customer(current_user)

    result = await db.execute(
        select(TripParcel, Trip)
        .join(Trip, Trip.id == TripParcel.trip_id)
        .where(
            TripParcel.id == parcel_id,
            Trip.customer_id == current_user.id,
            Trip.service_type == ServiceType.PARCEL,
        )
    )

    row = result.first()

    if not row:
        raise HTTPException(status_code=404, detail="Parcel not found")

    parcel, trip = row

    if trip.status != TripStatus.PENDING_CONFIRMATION:
        raise HTTPException(
            status_code=400,
            detail="Parcel booking already confirmed or cannot be confirmed",
        )

    trip.status = TripStatus.SEARCHING_DRIVER
    parcel.status = ParcelStatus.PENDING.value
    trip.updated_at = datetime.utcnow()

    await db.commit()
    await db.refresh(trip)
    await db.refresh(parcel)

    return {
        "message": "Parcel booking confirmed successfully. Searching for driver.",
        "trip_id": trip.id,
        "parcel_id": parcel.id,
        "trip_status": trip.status,
        "parcel_status": parcel.status,
        "delivery_charge": trip.fare,
    }


@router.get("/active")
async def get_active_parcel(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ensure_customer(current_user)

    result = await db.execute(
        select(Trip)
        .where(
            Trip.customer_id == current_user.id,
            Trip.service_type == ServiceType.PARCEL,
            Trip.status.in_(
                [
                    TripStatus.PENDING_CONFIRMATION,
                    TripStatus.SEARCHING_DRIVER,
                    TripStatus.DRIVER_ASSIGNED,
                    TripStatus.DRIVER_ARRIVED,
                    TripStatus.IN_PROGRESS,
                ]
            ),
        )
        .order_by(desc(Trip.created_at))
    )

    trip = result.scalar_one_or_none()

    if not trip:
        return {
            "message": "No active parcel booking",
            "data": None,
        }

    parcel_result = await db.execute(
        select(TripParcel).where(TripParcel.trip_id == trip.id)
    )

    parcel = parcel_result.scalar_one_or_none()

    return {
        "trip_id": trip.id,
        "parcel_id": parcel.id if parcel else None,
        "trip_status": trip.status,
        "parcel_status": parcel.status if parcel else None,
        "driver_id": trip.driver_id,
        "fare": trip.fare,
        "estimated_distance": trip.estimated_distance,
        "vehicle_category": trip.vehicle_category,
        "pickup_address": trip.pickup_address,
        "drop_address": trip.drop_address,
        "created_at": trip.created_at,
    }


@router.get("/{parcel_id}/track")
async def track_parcel(
    parcel_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ensure_customer(current_user)

    result = await db.execute(
        select(TripParcel, Trip)
        .join(Trip, Trip.id == TripParcel.trip_id)
        .where(
            TripParcel.id == parcel_id,
            Trip.customer_id == current_user.id,
        )
    )

    row = result.first()

    if not row:
        raise HTTPException(status_code=404, detail="Parcel not found")

    parcel, trip = row

    location_result = await db.execute(
        select(TripLocation)
        .where(TripLocation.trip_id == trip.id)
        .order_by(TripLocation.recorded_at)
    )

    locations = location_result.scalars().all()

    return {
        "trip_id": trip.id,
        "parcel_id": parcel.id,
        "trip_status": trip.status,
        "parcel_status": parcel.status,
        "driver_id": trip.driver_id,
        "fare": trip.fare,
        "estimated_distance": trip.estimated_distance,
        "vehicle_category": trip.vehicle_category,
        "pickup_address": trip.pickup_address,
        "drop_address": trip.drop_address,
        "receiver_name": parcel.receiver_name,
        "receiver_phone": parcel.receiver_phone,
        "receiver_address": parcel.receiver_address,
        "package_type": parcel.package_type,
        "weight_kg": parcel.weight_kg,
        "locations": [
            {
                "lat": float(location.lat),
                "lng": float(location.lng),
                "recorded_at": location.recorded_at,
            }
            for location in locations
        ],
    }


@router.get("/history/list")
async def parcel_history(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ensure_customer(current_user)

    result = await db.execute(
        select(TripParcel, Trip)
        .join(Trip, Trip.id == TripParcel.trip_id)
        .where(
            Trip.customer_id == current_user.id,
            Trip.service_type == ServiceType.PARCEL,
        )
        .order_by(desc(Trip.created_at))
    )

    rows = result.all()

    return [
        {
            "trip_id": trip.id,
            "parcel_id": parcel.id,
            "trip_status": trip.status,
            "parcel_status": parcel.status,
            "fare": trip.fare,
            "estimated_distance": trip.estimated_distance,
            "vehicle_category": trip.vehicle_category,
            "pickup_address": trip.pickup_address,
            "drop_address": trip.drop_address,
            "created_at": trip.created_at,
            "completed_at": trip.completed_at,
        }
        for parcel, trip in rows
    ]


@router.put("/{parcel_id}/cancel")
async def cancel_parcel(
    parcel_id: UUID,
    reason: str = Query(..., min_length=3),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ensure_customer(current_user)

    result = await db.execute(
        select(TripParcel, Trip)
        .join(Trip, Trip.id == TripParcel.trip_id)
        .where(
            TripParcel.id == parcel_id,
            Trip.customer_id == current_user.id,
        )
    )

    row = result.first()

    if not row:
        raise HTTPException(status_code=404, detail="Parcel not found")

    parcel, trip = row

    if trip.status in [TripStatus.IN_PROGRESS, TripStatus.COMPLETED]:
        raise HTTPException(
            status_code=400,
            detail="Parcel cannot be cancelled after pickup",
        )

    if trip.status == TripStatus.CANCELLED:
        raise HTTPException(
            status_code=409,
            detail="Parcel already cancelled",
        )

    trip.status = TripStatus.CANCELLED
    trip.cancelled_at = datetime.utcnow()
    trip.cancel_reason = reason
    parcel.status = ParcelStatus.CANCELLED.value
    trip.updated_at = datetime.utcnow()

    await db.commit()

    return {
        "message": "Parcel cancelled successfully",
        "trip_id": trip.id,
        "parcel_id": parcel.id,
    }