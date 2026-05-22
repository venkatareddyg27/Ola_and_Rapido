import random

from uuid import UUID

from datetime import datetime

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query
)

from sqlalchemy import (
    select,
    desc,
    and_
)

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.core.database import (
    get_db
)

from app.models.trips import (
    Trip
)

from app.models.user_models import (
    User
)

from app.models.support import (
    Rating
)

from app.schemas.trips import (
    TripCreate,
    TripResponse,
    TripEstimateRequest,
    TripEstimateResponse,
    TripRatingRequest
)

from app.core.enums import (
    TripStatus,
    UserRole
)

from app.core.security import (
    get_current_user
)

from app.services.matching import (
    DriverMatchingService
)

from app.services.fare import (
    FareCalculatorService
)

from app.services.distance_service import (
    DistanceService
)

router = APIRouter(

    prefix="/trips",

    tags=["Customer Trips"]
)

# =========================================================
# CUSTOMER ROLE CHECK
# =========================================================

def require_customer_role(
    current_user: User
):

    if current_user.role != UserRole.CUSTOMER:

        raise HTTPException(

            status_code=403,

            detail=
            "Only customers can access this API"
        )

# =========================================================
# ESTIMATE RIDE
# =========================================================

@router.post(
    "/estimate",
    response_model=TripEstimateResponse
)
async def estimate_trip(

    payload: TripEstimateRequest,

    current_user: User = Depends(
        get_current_user
    )
):

    # =====================================================
    # CUSTOMER CHECK
    # =====================================================

    require_customer_role(
        current_user
    )

    # =====================================================
    # CALCULATE DISTANCE
    # =====================================================

    distance_km = (
        DistanceService.calculate_distance(

            float(payload.pickup_lat),
            float(payload.pickup_lng),

            float(payload.drop_lat),
            float(payload.drop_lng)
        )
    )

    # =====================================================
    # CALCULATE FARE
    # =====================================================

    fare_details = (
        FareCalculatorService.calculate_fare(

            vehicle_category=
            payload.vehicle_category,

            distance_km=
            distance_km
        )
    )

    # =====================================================
    # RESPONSE
    # =====================================================

    return {

        "vehicle_category":
        payload.vehicle_category,

        "distance_km":
        distance_km,

        "estimated_fare":
        fare_details["total_fare"],

        "fare_breakdown":
        fare_details
    }

# =========================================================
# BOOK RIDE
# =========================================================

@router.post(
    "/book",
    response_model=TripResponse
)
async def book_trip(

    payload: TripCreate,

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    # =====================================================
    # CUSTOMER CHECK
    # =====================================================

    require_customer_role(
        current_user
    )

    # =====================================================
    # VALIDATE COORDINATES
    # =====================================================

    if not all([

        payload.pickup_lat,
        payload.pickup_lng,

        payload.drop_lat,
        payload.drop_lng
    ]):

        raise HTTPException(

            status_code=400,

            detail=
            "Coordinates are required"
        )

    # =====================================================
    # CALCULATE DISTANCE
    # =====================================================

    distance_km = (
        DistanceService.calculate_distance(

            float(payload.pickup_lat),
            float(payload.pickup_lng),

            float(payload.drop_lat),
            float(payload.drop_lng)
        )
    )

    # =====================================================
    # CALCULATE FARE
    # =====================================================

    fare_details = (
        FareCalculatorService.calculate_fare(

            vehicle_category=
            payload.vehicle_category,

            distance_km=
            distance_km
        )
    )

    # =====================================================
    # GENERATE OTP
    # =====================================================

    ride_otp = str(
        random.randint(1000, 9999)
    )

    # =====================================================
    # CREATE TRIP
    # =====================================================

    trip = Trip(

        customer_id=current_user.id,

        pickup_address=
        payload.pickup_address,

        drop_address=
        payload.drop_address,

        pickup_lat=
        payload.pickup_lat,

        pickup_lng=
        payload.pickup_lng,

        drop_lat=
        payload.drop_lat,

        drop_lng=
        payload.drop_lng,

        service_type=
        payload.service_type,

        fare=
        fare_details["total_fare"],

        estimated_distance=
        distance_km,

        estimated_fare=
        fare_details["total_fare"],

        vehicle_category=
        payload.vehicle_category,

        ride_otp=
        ride_otp,

        status=
        TripStatus.SEARCHING_DRIVER
    )

    db.add(trip)

    await db.commit()

    await db.refresh(trip)

    # =====================================================
    # MATCH DRIVER
    # =====================================================

    matching_service = (
        DriverMatchingService(
            db=db
        )
    )

    accepted_driver = (
        await matching_service.match_driver(

            trip_id=trip.id,

            pickup_lat=float(
                payload.pickup_lat
            ),

            pickup_lng=float(
                payload.pickup_lng
            ),

            vehicle_category=
            payload.vehicle_category.value
        )
    )

    # =====================================================
    # NO DRIVER FOUND
    # =====================================================

    if not accepted_driver:

        trip.status = (
            TripStatus.NO_DRIVER_FOUND
        )

        await db.commit()

        raise HTTPException(

            status_code=404,

            detail=
            "No nearby drivers found"
        )

    # =====================================================
    # ASSIGN DRIVER
    # =====================================================

    trip.driver_id = UUID(
        accepted_driver
    )

    trip.status = (
        TripStatus.DRIVER_ASSIGNED
    )

    await db.commit()

    await db.refresh(trip)

    return trip

# =========================================================
# GET ACTIVE TRIP
# =========================================================

@router.get(
    "/active",
    response_model=TripResponse
)
async def get_active_trip(

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    # =====================================================
    # CUSTOMER CHECK
    # =====================================================

    require_customer_role(
        current_user
    )

    result = await db.execute(

        select(Trip).where(

            and_(

                Trip.customer_id ==
                current_user.id,

                Trip.status.in_([

                    TripStatus.SEARCHING_DRIVER,

                    TripStatus.DRIVER_ASSIGNED,

                    TripStatus.DRIVER_ARRIVED,

                    TripStatus.IN_PROGRESS
                ])
            )
        )
    )

    trip = result.scalars().first()

    if not trip:

        raise HTTPException(

            status_code=404,

            detail="No active trip"
        )

    return trip

# =========================================================
# GET TRIP DETAILS
# =========================================================

@router.get(
    "/{trip_id}",
    response_model=TripResponse
)
async def get_trip(

    trip_id: UUID,

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    # =====================================================
    # CUSTOMER CHECK
    # =====================================================

    require_customer_role(
        current_user
    )

    result = await db.execute(

        select(Trip).where(

            Trip.id == trip_id,

            Trip.customer_id ==
            current_user.id
        )
    )

    trip = result.scalars().first()

    if not trip:

        raise HTTPException(

            status_code=404,

            detail="Trip not found"
        )

    return trip

# =========================================================
# GET TRIP HISTORY
# =========================================================

@router.get("/history")
async def get_trip_history(

    page: int = Query(
        1,
        ge=1
    ),

    limit: int = Query(
        10,
        le=100
    ),

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    # =====================================================
    # CUSTOMER CHECK
    # =====================================================

    require_customer_role(
        current_user
    )

    offset = (
        (page - 1) * limit
    )

    result = await db.execute(

        select(Trip)

        .where(
            Trip.customer_id ==
            current_user.id
        )

        .order_by(
            desc(Trip.created_at)
        )

        .offset(offset)

        .limit(limit)
    )

    trips = result.scalars().all()

    return {

        "page":
        page,

        "limit":
        limit,

        "total":
        len(trips),

        "data":
        trips
    }

# =========================================================
# CANCEL TRIP
# =========================================================

@router.put("/{trip_id}/cancel")
async def cancel_trip(

    trip_id: UUID,

    reason: str,

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    # =====================================================
    # CUSTOMER CHECK
    # =====================================================

    require_customer_role(
        current_user
    )

    result = await db.execute(

        select(Trip).where(

            Trip.id == trip_id,

            Trip.customer_id ==
            current_user.id
        )
    )

    trip = result.scalars().first()

    if not trip:

        raise HTTPException(

            status_code=404,

            detail="Trip not found"
        )

    if trip.status in [

        TripStatus.COMPLETED,

        TripStatus.CANCELLED
    ]:

        raise HTTPException(

            status_code=400,

            detail="Trip already ended"
        )

    trip.status = (
        TripStatus.CANCELLED
    )

    trip.cancel_reason = (
        reason
    )

    trip.cancelled_at = (
        datetime.utcnow()
    )

    await db.commit()

    return {

        "message":
        "Trip cancelled successfully"
    }

# =========================================================
# RATE DRIVER
# =========================================================

@router.post("/{trip_id}/rate")
async def rate_trip(

    trip_id: UUID,

    payload: TripRatingRequest,

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    # =====================================================
    # CUSTOMER CHECK
    # =====================================================

    require_customer_role(
        current_user
    )

    result = await db.execute(

        select(Trip).where(

            Trip.id == trip_id,

            Trip.customer_id ==
            current_user.id
        )
    )

    trip = result.scalars().first()

    if not trip:

        raise HTTPException(

            status_code=404,

            detail="Trip not found"
        )

    if trip.status != (
        TripStatus.COMPLETED
    ):

        raise HTTPException(

            status_code=400,

            detail="Trip not completed"
        )

    rating = Rating(

        trip_id=trip.id,

        rater_id=current_user.id,

        ratee_id=trip.driver_id,

        score=payload.score,

        comment=payload.comment
    )

    db.add(rating)

    trip.is_customer_rated = True

    await db.commit()

    return {

        "message":
        "Driver rated successfully"
    }