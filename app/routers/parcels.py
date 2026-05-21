
from uuid import UUID
from decimal import Decimal
from datetime import datetime

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy import select

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.core.database import get_db

from app.models.trips import (
    Trip,
    TripLocation
)
from app.models.trips import (
    TripParcel
)


from app.models.user_models import (
    User
)

from app.schemas.trips import (
    ParcelCreate,
    ParcelResponse
)

from app.core.enums import (
    TripStatus,
    ServiceType
)

from app.core.security import (
    get_current_user
)

from app.services.matching import (
    DriverMatchingService
)

from app.core.websocket_manager import (
    websocket_manager
)

from app.core.redis import (
    redis_client
)

router = APIRouter(
    prefix="/parcels",
    tags=["Parcels"]
)


# =========================================================
# CREATE PARCEL
# =========================================================

@router.post(
    "/book",
    response_model=ParcelResponse
)
async def create_parcel(
    payload: ParcelCreate,

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    # =====================================================
    # CREATE TRIP
    # =====================================================

    trip = Trip(
        customer_id=current_user.id,

        pickup_address="Pickup Address",

        drop_address=payload.receiver_address,

        service_type=ServiceType.PARCEL,

        fare=Decimal("120.00"),

        status=TripStatus.SEARCHING_DRIVER
    )

    db.add(trip)

    await db.commit()

    await db.refresh(trip)

    # =====================================================
    # CREATE PARCEL
    # =====================================================

    parcel = TripParcel(
        trip_id=trip.id,

        sender_name=payload.sender_name,
        sender_phone=payload.sender_phone,

        receiver_name=payload.receiver_name,
        receiver_phone=payload.receiver_phone,

        receiver_address=payload.receiver_address,

        package_type=payload.package_type,

        weight_kg=payload.weight_kg,

        cod_amount=payload.cod_amount,

        pod_otp="5678",

        status="created"
    )

    db.add(parcel)

    await db.commit()

    await db.refresh(parcel)

    # =====================================================
    # DRIVER MATCHING
    # =====================================================

    matching_service = DriverMatchingService(
        db=db,
        redis_client=redis_client,
        websocket_manager=websocket_manager
    )

    accepted_driver = await matching_service.match_driver(
        trip_id=trip.id,
        pickup_lat=0,
        pickup_lng=0,
        vehicle_category="bike"
    )

    if not accepted_driver:

        trip.status = TripStatus.NO_DRIVER_FOUND

        await db.commit()

        raise HTTPException(
            status_code=404,
            detail="No parcel driver available"
        )

    trip.driver_id = accepted_driver

    trip.status = TripStatus.DRIVER_ASSIGNED

    await db.commit()

    # =====================================================
    # SEND EVENT
    # =====================================================

    await websocket_manager.send_to_user(
        user_id=str(current_user.id),
        message={
            "event": "PARCEL_DRIVER_ASSIGNED",
            "trip_id": str(trip.id),
            "driver_id": str(accepted_driver)
        }
    )

    return parcel


# =========================================================
# TRACK PARCEL
# =========================================================

@router.get("/{parcel_id}/track")
async def track_parcel(
    parcel_id: UUID,

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    # =====================================================
    # GET PARCEL
    # =====================================================

    result = await db.execute(
        select(TripParcel).where(
            TripParcel.id == parcel_id
        )
    )

    parcel = result.scalars().first()

    if not parcel:

        raise HTTPException(
            status_code=404,
            detail="Parcel not found"
        )

    # =====================================================
    # GET TRIP
    # =====================================================

    trip_result = await db.execute(
        select(Trip).where(
            Trip.id == parcel.trip_id
        )
    )

    trip = trip_result.scalars().first()

    # =====================================================
    # LIVE LOCATION
    # =====================================================

    live_location = None

    if trip.driver_id:

        live_location = await redis_client.get(
            f"driver_location:{trip.driver_id}"
        )

    # =====================================================
    # LOCATION HISTORY
    # =====================================================

    location_result = await db.execute(
        select(TripLocation).where(
            TripLocation.trip_id == trip.id
        )
    )

    locations = (
        location_result.scalars().all()
    )

    return {
        "parcel_id": str(parcel.id),

        "status": parcel.status,

        "trip_status": trip.status,

        "driver_id": (
            str(trip.driver_id)
            if trip.driver_id else None
        ),

        "live_location": live_location,

        "locations": locations,

        "receiver_name": (
            parcel.receiver_name
        ),

        "receiver_phone": (
            parcel.receiver_phone
        ),

        "receiver_address": (
            parcel.receiver_address
        )
    }


# =========================================================
# DRIVER ACCEPT PARCEL
# =========================================================

@router.put("/{parcel_id}/accept")
async def accept_parcel(
    parcel_id: UUID,

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    result = await db.execute(
        select(TripParcel).where(
            TripParcel.id == parcel_id
        )
    )

    parcel = result.scalars().first()

    if not parcel:

        raise HTTPException(
            status_code=404,
            detail="Parcel not found"
        )

    trip_result = await db.execute(
        select(Trip).where(
            Trip.id == parcel.trip_id
        )
    )

    trip = trip_result.scalars().first()

    trip.driver_id = current_user.id

    trip.status = TripStatus.DRIVER_ASSIGNED

    parcel.status = "accepted"

    await db.commit()

    return {
        "message": "Parcel accepted successfully"
    }


# =========================================================
# PICKUP PARCEL BY OTP
# =========================================================

@router.put("/{parcel_id}/pickup")
async def pickup_parcel(
    parcel_id: UUID,
    otp: str,

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    result = await db.execute(
        select(TripParcel).where(
            TripParcel.id == parcel_id
        )
    )

    parcel = result.scalars().first()

    if not parcel:

        raise HTTPException(
            status_code=404,
            detail="Parcel not found"
        )

    # =====================================================
    # VERIFY OTP
    # =====================================================

    if parcel.pod_otp != otp:

        raise HTTPException(
            status_code=400,
            detail="Invalid OTP"
        )

    # =====================================================
    # UPDATE STATUS
    # =====================================================

    parcel.status = "picked"

    trip_result = await db.execute(
        select(Trip).where(
            Trip.id == parcel.trip_id
        )
    )

    trip = trip_result.scalars().first()

    trip.status = TripStatus.IN_PROGRESS

    await db.commit()

    return {
        "message": "Parcel picked successfully"
    }


# =========================================================
# DROP PARCEL BY OTP
# =========================================================

@router.put("/{parcel_id}/drop")
async def drop_parcel(
    parcel_id: UUID,
    otp: str,

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    result = await db.execute(
        select(TripParcel).where(
            TripParcel.id == parcel_id
        )
    )

    parcel = result.scalars().first()

    if not parcel:

        raise HTTPException(
            status_code=404,
            detail="Parcel not found"
        )

    # =====================================================
    # VERIFY OTP
    # =====================================================

    if parcel.pod_otp != otp:

        raise HTTPException(
            status_code=400,
            detail="Invalid OTP"
        )

    # =====================================================
    # COMPLETE DELIVERY
    # =====================================================

    parcel.status = "delivered"

    trip_result = await db.execute(
        select(Trip).where(
            Trip.id == parcel.trip_id
        )
    )

    trip = trip_result.scalars().first()

    trip.status = TripStatus.COMPLETED

    await db.commit()

    # =====================================================
    # SEND EVENT
    # =====================================================

    await websocket_manager.send_to_user(
        user_id=str(trip.customer_id),
        message={
            "event": "PARCEL_DELIVERED",
            "parcel_id": str(parcel.id)
        }
    )

    return {
        "message": "Parcel delivered successfully"
    }