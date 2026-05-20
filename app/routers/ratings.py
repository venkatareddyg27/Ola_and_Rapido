
from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy import (
    select,
    func,
    desc
)

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.core.database import get_db

from app.models.support import (
    Rating
)

from app.models.trips import (
    Trip
)

from app.models.users import (
    User,
    DriverProfile
)

from app.schemas.support import (
    RatingCreate,
    RatingResponse
)

from app.core.security import (
    get_current_user
)

from app.core.enums import (
    TripStatus
)

router = APIRouter(
    prefix="/ratings",
    tags=["Ratings"]
)


# =========================================================
# SUBMIT RATING
# =========================================================

@router.post(
    "/",
    response_model=RatingResponse
)
async def submit_rating(
    payload: RatingCreate,

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):
    """
    Submit rating and feedback
    for completed trip.
    """

    # =====================================================
    # GET TRIP
    # =====================================================

    result = await db.execute(
        select(Trip).where(
            Trip.id == payload.trip_id,

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

    # =====================================================
    # VALIDATE TRIP STATUS
    # =====================================================

    if trip.status != (
        TripStatus.COMPLETED
    ):

        raise HTTPException(
            status_code=400,
            detail="Trip not completed"
        )

    # =====================================================
    # CHECK EXISTING RATING
    # =====================================================

    existing_result = await db.execute(
        select(Rating).where(
            Rating.trip_id ==
            payload.trip_id,

            Rating.rater_id ==
            current_user.id
        )
    )

    existing_rating = (
        existing_result
        .scalars()
        .first()
    )

    if existing_rating:

        raise HTTPException(
            status_code=400,
            detail="Trip already rated"
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

    # =====================================================
    # UPDATE DRIVER RATING
    # =====================================================

    driver_result = await db.execute(
        select(DriverProfile).where(
            DriverProfile.id ==
            trip.driver_id
        )
    )

    driver = (
        driver_result
        .scalars()
        .first()
    )

    if driver:

        avg_result = await db.execute(

            select(
                func.avg(Rating.stars),
                func.count(Rating.id)
            )

            .where(
                Rating.ratee_id ==
                trip.driver_id
            )
        )

        avg_rating, total_count = (
            avg_result.first()
        )

        driver.rating = round(
            float(avg_rating or 5),
            2
        )

        driver.total_trips = (
            total_count or 0
        )

    # =====================================================
    # UPDATE TRIP
    # =====================================================

    trip.is_rated = True

    await db.commit()

    await db.refresh(rating)

    return rating


# =========================================================
# GET DRIVER RATINGS
# =========================================================

@router.get("/driver/{driver_id}")
async def get_driver_rating(
    driver_id: UUID,

    page: int = 1,

    limit: int = 10,

    db: AsyncSession = Depends(get_db)
):
    """
    Get driver's ratings,
    average rating,
    and total ratings count.
    """

    offset = (page - 1) * limit

    # =====================================================
    # DRIVER EXISTS
    # =====================================================

    driver_result = await db.execute(
        select(DriverProfile).where(
            DriverProfile.id ==
            driver_id
        )
    )

    driver = (
        driver_result
        .scalars()
        .first()
    )

    if not driver:

        raise HTTPException(
            status_code=404,
            detail="Driver not found"
        )

    # =====================================================
    # GET RATINGS
    # =====================================================

    ratings_result = await db.execute(

        select(Rating)

        .where(
            Rating.ratee_id ==
            driver_id
        )

        .order_by(
            desc(Rating.created_at)
        )

        .offset(offset)

        .limit(limit)
    )

    ratings = (
        ratings_result
        .scalars()
        .all()
    )

    # =====================================================
    # GET AVERAGE RATING
    # =====================================================

    avg_result = await db.execute(

        select(
            func.avg(Rating.stars),
            func.count(Rating.id)
        )

        .where(
            Rating.ratee_id ==
            driver_id
        )
    )

    avg_rating, total_ratings = (
        avg_result.first()
    )

    return {

        "driver_id":
        str(driver_id),

        "average_rating":
        round(
            float(avg_rating or 0),
            2
        ),

        "total_ratings":
        total_ratings,

        "ratings":
        ratings
    }