from uuid import UUID
from decimal import Decimal
from datetime import datetime, timedelta

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status
)

from sqlalchemy import (
    select,
    and_
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

from app.models.vehicles import Vehicle
from app.models.rentals import (
    Rental,
    RentalInspection
)
from app.models.support import Dispute

from app.schemas.rentals import (
    RentalCreate,
    RentalDisputeRequest,
    RentalUpdate,
    RentalResponse,
    RentalInspectionCreate,
    RentalInspectionUpdate,
    RentalInspectionResponse,
   )

from app.core.enums import (
    RentalStatus,
    DepositStatus
)


router = APIRouter(
    prefix="/rentals",
    tags=["Rentals"]
)


# =========================================================
# GET AVAILABLE RENTAL VEHICLES
# =========================================================

@router.get("/vehicles")
async def browse_rental_vehicles(

    lat: float | None = Query(None),

    lng: float | None = Query(None),

    category: str | None = Query(None),

    start_date: str | None = Query(None),

    end_date: str | None = Query(None),

    max_price: float | None = Query(None),

    db: AsyncSession = Depends(get_db)
):

    query = select(Vehicle)

    # =====================================================
    # CATEGORY FILTER
    # =====================================================

    if category:

        query = query.where(
            Vehicle.category == category
        )

    # =====================================================
    # PRICE FILTER
    # =====================================================

    if max_price:

        query = query.where(
            Vehicle.daily_rate <= max_price
        )

    result = await db.execute(query)

    vehicles = result.scalars().all()

    return {
        "success": True,
        "count": len(vehicles),
        "items": vehicles
    }


# =========================================================
# BOOK RENTAL VEHICLE
# =========================================================

@router.post("/book")
async def book_rental_vehicle(

    payload: RentalCreate,

    db: AsyncSession = Depends(get_db)
):

    # =====================================================
    # GET VEHICLE
    # =====================================================

    vehicle_query = await db.execute(

        select(Vehicle).where(
            Vehicle.id == payload.vehicle_id
        )
    )

    vehicle = vehicle_query.scalar_one_or_none()

    if not vehicle:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found"
        )

    # =====================================================
    # CHECK OVERLAPPING BOOKINGS
    # =====================================================

    overlap_query = await db.execute(

        select(Rental).where(
            and_(
                Rental.vehicle_id == payload.vehicle_id,

                Rental.status.in_([
                    RentalStatus.BOOKED,
                    RentalStatus.ACTIVE
                ])
            )
        )
    )

    existing_booking = overlap_query.scalar_one_or_none()

    if existing_booking:

        raise HTTPException(
            status_code=400,
            detail="Vehicle already booked"
        )

    # =====================================================
    # CALCULATE RENTAL DAYS
    # =====================================================

    total_days = (
        payload.end_date -
        payload.start_date
    ).days

    if total_days <= 0:

        raise HTTPException(
            status_code=400,
            detail="Invalid rental duration"
        )

    # =====================================================
    # CALCULATE FARE
    # =====================================================

    daily_rate = Decimal(vehicle.daily_rate)

    total_fare = daily_rate * total_days

    deposit_amount = Decimal("5000.00")

    # =====================================================
    # CREATE RENTAL
    # =====================================================

    rental = Rental(

        vehicle_id=vehicle.id,

        renter_id=vehicle.owner_id,

        owner_id=vehicle.owner_id,

        pickup_time=datetime.combine(
            payload.start_date,
            datetime.min.time()
        ),

        drop_time=datetime.combine(
            payload.end_date,
            datetime.min.time()
        ),

        daily_rate=daily_rate,

        deposit_amount=deposit_amount,

        total_fare=total_fare,

        status=RentalStatus.BOOKED,

        deposit_status=DepositStatus.PENDING
    )

    db.add(rental)

    await db.commit()

    await db.refresh(rental)

    return {
        "success": True,
        "message": "Rental booked successfully",
        "rental_id": rental.id,
        "total_fare": total_fare,
        "deposit_amount": deposit_amount
    }


# =========================================================
# SUBMIT RENTAL INSPECTION
# =========================================================

@router.post("/{rental_id}/inspection")
async def submit_rental_inspection(

    rental_id: UUID,

    payload:RentalInspectionCreate,

    db: AsyncSession = Depends(get_db)
):

    # =====================================================
    # GET RENTAL
    # =====================================================

    rental_query = await db.execute(

        select(Rental).where(
            Rental.id == rental_id
        )
    )

    rental = rental_query.scalar_one_or_none()

    if not rental:

        raise HTTPException(
            status_code=404,
            detail="Rental not found"
        )

    # =====================================================
    # CREATE INSPECTION
    # =====================================================

    inspection = RentalInspection(

        rental_id=rental.id,

        inspection_type=payload.inspection_type,

        damage_notes=payload.notes,

        photo_urls=payload.photo_urls,

        fuel_level=payload.fuel_level,

        odometer_reading=payload.odometer_reading,

        inspected_at=datetime.utcnow(),

        inspector_user_id=rental.owner_id
    )

    db.add(inspection)

    await db.commit()

    await db.refresh(inspection)

    return {
        "success": True,
        "message": "Inspection submitted successfully",
        "inspection_id": inspection.id
    }


# =========================================================
# COMPLETE RENTAL
# =========================================================

@router.put("/{rental_id}/complete")
async def complete_rental(

    rental_id: UUID,

    db: AsyncSession = Depends(get_db)
):

    rental_query = await db.execute(

        select(Rental).where(
            Rental.id == rental_id
        )
    )

    rental = rental_query.scalar_one_or_none()

    if not rental:

        raise HTTPException(
            status_code=404,
            detail="Rental not found"
        )

    rental.status = RentalStatus.COMPLETED

    rental.deposit_status = DepositStatus.REFUNDED

    await db.commit()

    return {
        "success": True,
        "message": "Rental completed successfully",
        "deposit_refunded": True
    }


# =========================================================
# RAISE RENTAL DISPUTE
# =========================================================

@router.post("/{rental_id}/dispute")
async def raise_rental_dispute(

    rental_id: UUID,

    payload: RentalDisputeRequest,

    db: AsyncSession = Depends(get_db)
):

    rental_query = await db.execute(

        select(Rental).where(
            Rental.id == rental_id
        )
    )

    rental = rental_query.scalar_one_or_none()

    if not rental:

        raise HTTPException(
            status_code=404,
            detail="Rental not found"
        )

    dispute = Dispute(

        rental_id=rental.id,

        reason=payload.reason,

        description=payload.description,

        damage_claim_amount=payload.damage_amount,

        status="OPEN",

        created_at=datetime.utcnow()
    )

    db.add(dispute)

    await db.commit()

    await db.refresh(dispute)

    return {
        "success": True,
        "message": "Dispute raised successfully",
        "dispute_id": dispute.id
    }