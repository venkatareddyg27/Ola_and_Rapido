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

from app.schemas.trips import ParcelCreate, ParcelResponse

from app.services.fare import FareCalculatorService
from app.services.matching import DriverMatchingService
from app.services.distance_service import DistanceService

from app.core.websocket_manager import websocket_manager


router = APIRouter(
    prefix="/customer/parcels",
    tags=["Customer Parcels"],
)


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


@router.get("/fare-estimate")
async def estimate_parcel_fare(
    pickup_lat: Decimal = Query(...),
    pickup_lng: Decimal = Query(...),
    drop_lat: Decimal = Query(...),
    drop_lng: Decimal = Query(...),
    weight_kg: float = Query(..., ge=1, le=10),
    current_user: User = Depends(get_current_user),
):
    ensure_customer(current_user)

    vehicle_category = select_vehicle_by_weight(weight_kg)

    distance_km = DistanceService.calculate_distance(
        float(pickup_lat),
        float(pickup_lng),
        float(drop_lat),
        float(drop_lng),
    )

    fare_data = FareCalculatorService.calculate_fare(
        vehicle_category=vehicle_category,
        distance_km=distance_km,
        surge_multiplier=1.0,
        waiting_charge=0,
        toll_charge=0,
    )

    parcel_weight_charge = Decimal(str(weight_kg * 5))
    total_fare = Decimal(str(fare_data["total_fare"])) + parcel_weight_charge

    return {
        "service_type": ServiceType.PARCEL.value,
        "recommended_vehicle": vehicle_category.value,
        "distance_km": round(distance_km, 2),
        "weight_kg": weight_kg,
        "base_trip_fare": fare_data["total_fare"],
        "parcel_weight_charge": round(parcel_weight_charge, 2),
        "estimated_total_fare": round(total_fare, 2),
        "currency": "INR",
        "rule": "Bike supports up to 4kg. Above 4kg auto is assigned.",
    }


@router.post("/book", response_model=ParcelResponse)
async def book_parcel(
    payload: ParcelCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ensure_customer(current_user)

    weight_kg = float(payload.weight_kg)
    vehicle_category = select_vehicle_by_weight(weight_kg)

    # 1. Check active parcel trip
    active_result = await db.execute(
        select(Trip).where(
            Trip.customer_id == current_user.id,
            Trip.service_type == ServiceType.PARCEL,
            Trip.status.in_([
                TripStatus.SEARCHING_DRIVER,
                TripStatus.DRIVER_ASSIGNED,
                TripStatus.DRIVER_ARRIVED,
                TripStatus.IN_PROGRESS,
            ]),
        )
    )

    if active_result.scalar_one_or_none():
        raise HTTPException(
            status_code=409,
            detail="You already have an active parcel booking",
        )

    # 2. Calculate distance
    distance_km = DistanceService.calculate_distance(
        float(payload.pickup_lat),
        float(payload.pickup_lng),
        float(payload.drop_lat),
        float(payload.drop_lng),
    )

    # 3. Calculate fare
    fare_data = FareCalculatorService.calculate_fare(
        vehicle_category=vehicle_category,
        distance_km=distance_km,
        surge_multiplier=1.0,
        waiting_charge=0,
        toll_charge=0,
    )

    parcel_weight_charge = Decimal(str(weight_kg * 5))
    final_fare = Decimal(str(fare_data["total_fare"])) + parcel_weight_charge

    # 4. Create trip first
    trip = Trip(
        customer_id=current_user.id,
        pickup_address=payload.pickup_address,
        drop_address=payload.receiver_address,
        pickup_lat=payload.pickup_lat,
        pickup_lng=payload.pickup_lng,
        drop_lat=payload.drop_lat,
        drop_lng=payload.drop_lng,
        service_type=ServiceType.PARCEL,
        status=TripStatus.SEARCHING_DRIVER,
        fare=final_fare,
        surge_multiplier=Decimal("1.0"),
        otp=generate_otp(),
    )

    db.add(trip)
    await db.flush()

    # 5. Create parcel linked to trip
    parcel = TripParcel(
        trip_id=trip.id,
        sender_name=payload.sender_name,
        sender_phone=payload.sender_phone,
        receiver_name=payload.receiver_name,
        receiver_phone=payload.receiver_phone,
        receiver_address=payload.receiver_address,
        package_type=payload.package_type,
        weight_kg=payload.weight_kg,
        cod_amount=payload.cod_amount or Decimal("0.00"),
        pod_otp=generate_otp(),
        status=ParcelStatus.REQUESTED.value,
    )

    db.add(parcel)
    await db.flush()

    # 6. Match driver
    matching_service = DriverMatchingService(
        db=db,
        redis_client=redis_client,
        websocket_manager=websocket_manager,
    )

    accepted_driver = await matching_service.match_driver(
        trip_id=trip.id,
        pickup_lat=float(payload.pickup_lat),
        pickup_lng=float(payload.pickup_lng),
        vehicle_category=vehicle_category.value,
    )

    # 7. Update status based on driver availability
    if not accepted_driver:
        trip.status = TripStatus.NO_DRIVER_FOUND
        parcel.status = ParcelStatus.FAILED.value

        await db.commit()

        raise HTTPException(
            status_code=404,
            detail="No driver available for parcel booking",
        )

    trip.driver_id = accepted_driver
    trip.status = TripStatus.DRIVER_ASSIGNED
    parcel.status = ParcelStatus.DRIVER_ASSIGNED.value

    await db.commit()
    await db.refresh(parcel)

    # 8. Notify customer
    await websocket_manager.send_to_user(
        user_id=str(current_user.id),
        message={
            "event": "PARCEL_DRIVER_ASSIGNED",
            "trip_id": str(trip.id),
            "parcel_id": str(parcel.id),
            "driver_id": str(accepted_driver),
            "vehicle_category": vehicle_category.value,
            "distance_km": round(distance_km, 2),
            "fare": str(final_fare),
        },
    )

    return parcel

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
        "pickup_address": trip.pickup_address,
        "drop_address": trip.drop_address,
        "receiver_name": parcel.receiver_name,
        "receiver_phone": parcel.receiver_phone,
        "receiver_address": parcel.receiver_address,
        "package_type": parcel.package_type,
        "weight_kg": parcel.weight_kg,
        "cod_amount": parcel.cod_amount,
        "locations": locations,
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
    trip.cancellation_reason = reason

    parcel.status = ParcelStatus.CANCELLED.value

    await db.commit()

    return {
        "message": "Parcel cancelled successfully",
        "trip_id": trip.id,
        "parcel_id": parcel.id,
    }