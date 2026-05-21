from uuid import UUID
from datetime import datetime

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status
)

from sqlalchemy import (
    select,
    desc
)

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.core.database import get_db

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
    TripUpdate,
    TripResponse,
    TripEstimateRequest,
    TripEstimateResponse,
    TripRatingRequest
)

from app.core.enums import (
    TripStatus
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
    prefix="/trips",
    tags=["Trips"]
)

# =========================================================
# FARE CONFIG
# =========================================================

BASE_FARE = {
    "bike": 40,
    "auto": 80,
    "cab": 120
}

PER_KM_RATE = {
    "bike": 8,
    "auto": 12,
    "cab": 18
}


# =========================================================
# ESTIMATE TRIP
# =========================================================

@router.post(
    "/estimate",
    response_model=TripEstimateResponse
)
async def estimate_trip(
    payload: TripEstimateRequest
):
    """
    Calculate estimated fare.
    """

    category = (
        payload.vehicle_category
        .lower()
    )

    if category not in BASE_FARE:

        raise HTTPException(
            status_code=400,
            detail="Invalid category"
        )

    base_fare = BASE_FARE[category]

    distance_charge = (
        payload.distance_km *
        PER_KM_RATE[category]
    )

    estimated_fare = (
        base_fare +
        distance_charge
    )

    return {
        "vehicle_category": category,

        "distance_km":
        payload.distance_km,

        "estimated_fare":
        round(estimated_fare, 2)
    }


# =========================================================
# BOOK TRIP
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
    """
    Book ride with driver matching.
    """

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

        fare=payload.fare,

        status=
        TripStatus.SEARCHING_DRIVER,

        ride_otp="1234"
    )

    db.add(trip)

    await db.commit()

    await db.refresh(trip)

    # =====================================================
    # MATCH DRIVER
    # =====================================================

    matching_service = (
        DriverMatchingService(
            db=db,
            redis_client=redis_client,
            websocket_manager=
            websocket_manager
        )
    )

    accepted_driver = (
        await matching_service.match_driver(
            trip_id=trip.id,

            pickup_lat=float(
                payload.pickup_lat or 0
            ),

            pickup_lng=float(
                payload.pickup_lng or 0
            ),

            vehicle_category="bike"
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
            detail=(
                "No nearby drivers found"
            )
        )

    # =====================================================
    # ASSIGN DRIVER
    # =====================================================

    trip.driver_id = accepted_driver

    trip.status = (
        TripStatus.DRIVER_ASSIGNED
    )

    await db.commit()

    await db.refresh(trip)

    # =====================================================
    # REALTIME EVENT
    # =====================================================

    await websocket_manager.send_to_user(
        user_id=str(current_user.id),

        message={
            "event":
            "DRIVER_ASSIGNED",

            "trip_id":
            str(trip.id),

            "driver_id":
            str(accepted_driver)
        }
    )

    return trip


# =========================================================
# TRIP HISTORY
# =========================================================

@router.get("/history")
async def trip_history(
    page: int = Query(1, ge=1),

    limit: int = Query(10, le=100),

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):
    """
    Get trip history.
    """

    offset = (page - 1) * limit

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
        "page": page,
        "limit": limit,
        "data": trips
    }


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
    """
    Get trip details.
    """

    result = await db.execute(
        select(Trip).where(
            Trip.id == trip_id
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
    """
    Cancel trip.
    """

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

    # =====================================================
    # UPDATE STATUS
    # =====================================================

    trip.status = (
        TripStatus.CANCELLED
    )

    trip.cancel_reason = reason

    trip.cancelled_at = (
        datetime.utcnow()
    )

    await db.commit()

    # =====================================================
    # CLEAR REDIS
    # =====================================================

    await redis_client.delete(
        f"trip_matching:{trip_id}"
    )

    await redis_client.delete(
        f"trip_accepted:{trip_id}"
    )

    # =====================================================
    # NOTIFY DRIVER
    # =====================================================

    if trip.driver_id:

        await (
            websocket_manager
            .send_to_user(
                user_id=str(
                    trip.driver_id
                ),
                message={
                    "event":
                    "TRIP_CANCELLED",

                    "trip_id":
                    str(trip.id)
                }
            )
        )

    return {
        "message":
        "Trip cancelled successfully"
    }


# =========================================================
# RATE TRIP
# =========================================================

@router.put("/{trip_id}/rate")
async def rate_trip(
    trip_id: UUID,

    payload: TripRatingRequest,

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):
    """
    Rate completed trip.
    """

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

    # =====================================================
    # CREATE RATING
    # =====================================================

    rating = Rating(
        trip_id=trip.id,

        rater_id=current_user.id,

        ratee_id=trip.driver_id,

        stars=payload.stars,

        feedback=payload.feedback
    )

    db.add(rating)

    trip.is_rated = True

    await db.commit()

    return {
        "message":
        "Trip rated successfully"
    }