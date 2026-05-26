from uuid import UUID
from datetime import datetime, date
from decimal import Decimal

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy import (
    select,
    func,
    update
)

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.core.database import (
    get_db
)

from app.core.enums import (
    DriverStatus,
    TripStatus,
    UserRole
)

from app.core.security import (
    get_current_user
)

from app.models.user_models import (
    User,
    DriverProfile,
    DriverLocation
)

from app.models.trips import (
    Trip
)

from app.services.distance_service import (
    DistanceService
)

router = APIRouter(
    prefix="/drivers",
    tags=["Driver Trips"]
)

# =========================================================
# DRIVER ROLE VALIDATION
# =========================================================

def require_driver_role(
    current_user: User
):

    if current_user.role != UserRole.DRIVER:

        raise HTTPException(

            status_code=403,

            detail=
            "Only drivers can access this API"
        )

# =========================================================
# GET DRIVER PROFILE
# =========================================================

async def get_driver_profile(

    db: AsyncSession,

    user_id: UUID
):

    result = await db.execute(

        select(DriverProfile).where(
            DriverProfile.user_id == user_id
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
# UPDATE DRIVER STATUS
# =========================================================

@router.put("/status")
async def update_driver_status(

    status: DriverStatus,

    latitude: Decimal,

    longitude: Decimal,

    heading: Decimal | None = None,

    speed: Decimal | None = None,

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    require_driver_role(current_user)

    driver = await get_driver_profile(
        db,
        current_user.id
    )

    if not driver.is_verified:

        raise HTTPException(

            status_code=400,

            detail=
            "Admin approval pending"
        )

    if driver.status == DriverStatus.BLOCKED:

        raise HTTPException(

            status_code=403,

            detail=
            "Driver account blocked"
        )

    if not driver.vehicle_id:

        raise HTTPException(

            status_code=400,

            detail=
            "Vehicle not added"
        )

    driver.status = status

    await db.execute(

        update(DriverLocation)

        .where(
            DriverLocation.driver_id ==
            driver.id
        )

        .values(
            is_active=False
        )
    )

    is_active = (
        status == DriverStatus.ONLINE
    )

    location = DriverLocation(

        driver_id=driver.id,

        latitude=latitude,

        longitude=longitude,

        heading=heading,

        speed=speed,

        is_active=is_active
    )

    db.add(location)

    try:

        await db.commit()

    except Exception:

        await db.rollback()

        raise

    return {

        "message":
        "Driver status updated",

        "status":
        status
    }

# =========================================================
# NEARBY TRIPS
# =========================================================

@router.get("/nearby-trips")
async def get_nearby_trips(

    radius_km: float = 5,

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    require_driver_role(current_user)

    driver = await get_driver_profile(
        db,
        current_user.id
    )

    if driver.status != DriverStatus.ONLINE:

        raise HTTPException(

            status_code=400,

            detail=
            "Driver must be online"
        )

    location_result = await db.execute(

        select(DriverLocation).where(

            DriverLocation.driver_id ==
            driver.id,

            DriverLocation.is_active == True
        )
    )

    driver_location = (
        location_result.scalar_one_or_none()
    )

    if not driver_location:

        raise HTTPException(

            status_code=404,

            detail=
            "Driver location not found"
        )

    trip_result = await db.execute(

        select(Trip).where(

            Trip.status ==
            TripStatus.SEARCHING_DRIVER,

            Trip.driver_id == None
        )
    )

    trips = trip_result.scalars().all()

    nearby_trips = []

    for trip in trips:

        distance = (
            DistanceService.calculate_distance(

                float(driver_location.latitude),

                float(driver_location.longitude),

                float(trip.pickup_lat),

                float(trip.pickup_lng)
            )
        )

        if not DistanceService.is_serviceable_distance(

            distance,
            radius_km
        ):

            continue

        estimated_time = (
            DistanceService.estimate_duration(
                distance
            )
        )

        nearby_trips.append({

            "trip_id":
            str(trip.id),

            "pickup_latitude":
            float(trip.pickup_lat),

            "pickup_longitude":
            float(trip.pickup_lng),

            "drop_latitude":
            float(trip.drop_lat),

            "drop_longitude":
            float(trip.drop_lng),

            "estimated_fare":
            float(trip.estimated_fare),

            "distance_km":
            distance,

            "estimated_time_minutes":
            estimated_time
        })

    nearby_trips.sort(

        key=lambda x: x["distance_km"]
    )

    return {

        "count":
        len(nearby_trips),

        "trips":
        nearby_trips
    }

# =========================================================
# ACCEPT TRIP
# =========================================================

@router.put("/trips/{trip_id}/accept")
async def accept_trip(

    trip_id: UUID,

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    require_driver_role(current_user)

    driver = await get_driver_profile(
        db,
        current_user.id
    )

    if not driver.is_verified:

        raise HTTPException(

            status_code=403,

            detail=
            "Driver not verified"
        )

    if driver.status != DriverStatus.ONLINE:

        raise HTTPException(

            status_code=400,

            detail=
            "Driver is not online"
        )

    existing_trip_result = await db.execute(

        select(Trip).where(

            Trip.driver_id == driver.id,

            Trip.status.in_([

                TripStatus.DRIVER_ASSIGNED,

                TripStatus.DRIVER_ARRIVED,

                TripStatus.IN_PROGRESS
            ])
        )
    )

    active_trip = (
        existing_trip_result.scalar_one_or_none()
    )

    if active_trip:

        raise HTTPException(

            status_code=400,

            detail=
            "Driver already has active trip"
        )

    trip_result = await db.execute(

        select(Trip).where(
            Trip.id == trip_id
        )
    )

    trip = trip_result.scalar_one_or_none()

    if not trip:

        raise HTTPException(

            status_code=404,

            detail="Trip not found"
        )

    if trip.driver_id:

        raise HTTPException(

            status_code=400,

            detail=
            "Trip already assigned"
        )

    trip.driver_id = driver.id

    trip.status = (
        TripStatus.DRIVER_ASSIGNED
    )

    driver.status = (
        DriverStatus.ON_TRIP
    )

    try:

        await db.commit()

    except Exception:

        await db.rollback()

        raise

    return {

        "message":
        "Ride accepted"
    }

# =========================================================
# DRIVER ARRIVED
# =========================================================

@router.put("/trips/{trip_id}/arrived")
async def arrived_trip(

    trip_id: UUID,

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    require_driver_role(current_user)

    driver = await get_driver_profile(
        db,
        current_user.id
    )

    result = await db.execute(

        select(Trip).where(
            Trip.id == trip_id
        )
    )

    trip = result.scalar_one_or_none()

    if not trip:

        raise HTTPException(

            status_code=404,

            detail="Trip not found"
        )

    if trip.driver_id != driver.id:

        raise HTTPException(

            status_code=403,

            detail=
            "Trip does not belong to driver"
        )

    if trip.status != TripStatus.DRIVER_ASSIGNED:

        raise HTTPException(

            status_code=400,

            detail=
            "Trip is not assigned"
        )

    trip.status = (
        TripStatus.DRIVER_ARRIVED
    )

    await db.commit()

    return {

        "message":
        "Driver reached pickup"
    }

# =========================================================
# START TRIP
# =========================================================

@router.put("/trips/{trip_id}/start")
async def start_trip(

    trip_id: UUID,

    ride_otp: str,

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    require_driver_role(current_user)

    driver = await get_driver_profile(
        db,
        current_user.id
    )

    result = await db.execute(

        select(Trip).where(
            Trip.id == trip_id
        )
    )

    trip = result.scalar_one_or_none()

    if not trip:

        raise HTTPException(

            status_code=404,

            detail="Trip not found"
        )

    if trip.driver_id != driver.id:

        raise HTTPException(

            status_code=403,

            detail=
            "Trip does not belong to driver"
        )

    if trip.status != TripStatus.DRIVER_ARRIVED:

        raise HTTPException(

            status_code=400,

            detail=
            "Driver has not arrived"
        )

    if trip.ride_otp != ride_otp:

        raise HTTPException(

            status_code=400,

            detail="Invalid OTP"
        )

    trip.status = (
        TripStatus.IN_PROGRESS
    )

    trip.started_at = (
        datetime.utcnow()
    )

    await db.commit()

    return {

        "message":
        "Ride started"
    }

# =========================================================
# COMPLETE TRIP
# =========================================================

@router.put("/trips/{trip_id}/complete")
async def complete_trip(

    trip_id: UUID,

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    require_driver_role(current_user)

    driver = await get_driver_profile(
        db,
        current_user.id
    )

    trip_result = await db.execute(

        select(Trip).where(
            Trip.id == trip_id
        )
    )

    trip = trip_result.scalar_one_or_none()

    if not trip:

        raise HTTPException(

            status_code=404,

            detail="Trip not found"
        )

    if trip.driver_id != driver.id:

        raise HTTPException(

            status_code=403,

            detail=
            "Trip does not belong to driver"
        )

    if trip.status != TripStatus.IN_PROGRESS:

        raise HTTPException(

            status_code=400,

            detail=
            "Trip is not in progress"
        )

    trip.status = (
        TripStatus.COMPLETED
    )

    trip.completed_at = (
        datetime.utcnow()
    )

    driver.status = (
        DriverStatus.ONLINE
    )

    driver.total_trips += 1

    await db.commit()

    return {

        "message":
        "Ride completed"
    }

# =========================================================
# CANCEL TRIP
# =========================================================

@router.put("/trips/{trip_id}/cancel")
async def cancel_trip(

    trip_id: UUID,

    reason: str,

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    require_driver_role(current_user)

    driver = await get_driver_profile(
        db,
        current_user.id
    )

    result = await db.execute(

        select(Trip).where(
            Trip.id == trip_id
        )
    )

    trip = result.scalar_one_or_none()

    if not trip:

        raise HTTPException(

            status_code=404,

            detail="Trip not found"
        )

    if trip.driver_id != driver.id:

        raise HTTPException(

            status_code=403,

            detail=
            "Trip does not belong to driver"
        )

    if trip.status not in [

        TripStatus.DRIVER_ASSIGNED,
        TripStatus.DRIVER_ARRIVED

    ]:

        raise HTTPException(

            status_code=400,

            detail=
            "Trip cannot be cancelled"
        )

    trip.status = (
        TripStatus.CANCELLED
    )

    trip.cancel_reason = reason

    driver.status = (
        DriverStatus.ONLINE
    )

    await db.commit()

    return {

        "message":
        "Ride cancelled"
    }

# =========================================================
# CURRENT TRIP
# =========================================================

@router.get("/current-trip")
async def current_trip(

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    require_driver_role(current_user)

    driver = await get_driver_profile(
        db,
        current_user.id
    )

    trip_result = await db.execute(

        select(Trip).where(

            Trip.driver_id == driver.id,

            Trip.status.in_([

                TripStatus.DRIVER_ASSIGNED,

                TripStatus.DRIVER_ARRIVED,

                TripStatus.IN_PROGRESS
            ])
        )
    )

    trip = trip_result.scalar_one_or_none()

    if not trip:

        return {

            "message":
            "No active trip"
        }

    return trip

# =========================================================
# TODAY EARNINGS
# =========================================================

@router.get("/earnings/today")
async def today_earnings(

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    require_driver_role(current_user)

    driver = await get_driver_profile(
        db,
        current_user.id
    )

    today = date.today()

    result = await db.execute(

        select(
            func.sum(Trip.fare),
            func.count(Trip.id)
        ).where(

            Trip.driver_id == driver.id,

            Trip.status ==
            TripStatus.COMPLETED,

            func.date(
                Trip.completed_at
            ) == today
        )
    )

    earnings, rides = result.first()

    return {

        "today_earnings":
        float(earnings or 0),

        "rides_completed":
        rides or 0
    }