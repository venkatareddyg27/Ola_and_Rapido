from uuid import UUID
from decimal import Decimal
from datetime import datetime

from django import db
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import get_current_user

from app.models.user_models import User
from app.core.database import get_db
from app.models.vehicles import Vehicle
from app.models.rentals import Rental, RentalInspection
from app.models.support import Dispute

from app.schemas.rentals import (
    RentalCreate,
    RentalDisputeRequest,
    RentalDriverUpdate,
    RentalInspectionCreate,
    RentalDriverCreate,
    RentalDriverResponse
)

from app.core.enums import (
    RentalStatus,
    DepositStatus,
    DisputeStatus,
    DisputePriority,
    UserRole,
)
from app.models.rentals import RentalDriver

router = APIRouter(
    prefix="/rentals",
    tags=["Rentals"]
)


@router.get("/vehicles")
async def browse_rental_vehicles(
    lat: float | None = Query(None),
    lng: float | None = Query(None),
    category: str | None = Query(None),
    start_date: str | None = Query(None),
    end_date: str | None = Query(None),
    max_price: float | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    query = select(Vehicle)

    if category:
        query = query.where(Vehicle.category == category)

    if max_price:
        query = query.where(Vehicle.daily_rate <= max_price)

    result = await db.execute(query)
    vehicles = result.scalars().all()

    return {
        "success": True,
        "count": len(vehicles),
        "items": vehicles,
    }


@router.post("/book")
async def book_rental_vehicle(
    payload: RentalCreate,
    db: AsyncSession = Depends(get_db),
):
    vehicle_query = await db.execute(
        select(Vehicle).where(Vehicle.id == payload.vehicle_id)
    )
    vehicle = vehicle_query.scalar_one_or_none()

    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found",
        )

    overlap_query = await db.execute(
        select(Rental).where(
            and_(
                Rental.vehicle_id == payload.vehicle_id,
                Rental.status.in_([
                    RentalStatus.BOOKED,
                    RentalStatus.ACTIVE,
                ]),
            )
        )
    )

    existing_booking = overlap_query.scalar_one_or_none()

    if existing_booking:
        raise HTTPException(
            status_code=400,
            detail="Vehicle already booked",
        )

    total_days = (payload.end_date - payload.start_date).days

    if total_days <= 0:
        raise HTTPException(
            status_code=400,
            detail="Invalid rental duration",
        )

    daily_rate = Decimal(str(vehicle.daily_rate))
    total_fare = daily_rate * total_days
    deposit_amount = Decimal("5000.00")

    rental = Rental(
        vehicle_id=vehicle.id,
        renter_id=payload.renter_id,
        owner_id=payload.owner_id or vehicle.owner_id,
        pickup_time=datetime.combine(payload.start_date, datetime.min.time()),
        drop_time=datetime.combine(payload.end_date, datetime.min.time()),
        daily_rate=daily_rate,
        deposit_amount=deposit_amount,
        total_fare=total_fare,
        status=RentalStatus.BOOKED,
        deposit_status=DepositStatus.PENDING,
    )

    db.add(rental)
    await db.commit()
    await db.refresh(rental)

    return {
        "success": True,
        "message": "Rental booked successfully",
        "rental_id": rental.id,
        "total_fare": total_fare,
        "deposit_amount": deposit_amount,
    }


@router.post("/{rental_id}/inspection")
async def submit_rental_inspection(
    rental_id: UUID,
    payload: RentalInspectionCreate,
    db: AsyncSession = Depends(get_db),
):
    rental_query = await db.execute(
        select(Rental).where(Rental.id == rental_id)
    )
    rental = rental_query.scalar_one_or_none()

    if not rental:
        raise HTTPException(
            status_code=404,
            detail="Rental not found",
        )

    inspection = RentalInspection(
        rental_id=rental.id,
        inspection_type=payload.inspection_type,
        damage_notes=payload.damage_notes,
        photo_urls=payload.photo_urls,
        video_url=payload.video_url,
        fuel_level=payload.fuel_level,
        odometer_reading=payload.odometer_reading,
        inspected_at=payload.inspected_at or datetime.utcnow(),
        inspector_user_id=payload.inspector_user_id or rental.owner_id,
    )

    db.add(inspection)
    await db.commit()
    await db.refresh(inspection)

    return {
        "success": True,
        "message": "Inspection submitted successfully",
        "inspection_id": inspection.id,
    }


@router.put("/{rental_id}/complete")
async def complete_rental(
    rental_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    rental_query = await db.execute(
        select(Rental).where(Rental.id == rental_id)
    )
    rental = rental_query.scalar_one_or_none()

    if not rental:
        raise HTTPException(
            status_code=404,
            detail="Rental not found",
        )

    rental.status = RentalStatus.COMPLETED
    rental.deposit_status = DepositStatus.REFUNDED

    await db.commit()
    await db.refresh(rental)

    return {
        "success": True,
        "message": "Rental completed successfully",
        "deposit_refunded": True,
    }


@router.post("/{rental_id}/dispute")
async def raise_rental_dispute(
    rental_id: UUID,
    payload: RentalDisputeRequest,
    db: AsyncSession = Depends(get_db),
):
    rental_query = await db.execute(
        select(Rental).where(Rental.id == rental_id)
    )
    rental = rental_query.scalar_one_or_none()

    if not rental:
        raise HTTPException(
            status_code=404,
            detail="Rental not found",
        )

    dispute = Dispute(
        user_id=payload.user_id,
        rental_id=rental.id,
        category=payload.category,
        description=payload.description,
        priority=DisputePriority.MEDIUM,
        status=DisputeStatus.OPEN,
        created_at=datetime.utcnow(),
    )

    db.add(dispute)
    await db.commit()
    await db.refresh(dispute)

    return {
        "success": True,
        "message": "Dispute raised successfully",
        "dispute_id": dispute.id,
    }

@router.post("/", response_model=RentalDriverResponse)
async def create_rental_driver(
    payload: RentalDriverCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
  
    if current_user.role != UserRole.RENTER and payload.renter_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Only renters can book drivers for themselves"
        )
     
    rental_driver = RentalDriver(
        renter_id=current_user.id,
        no_of_seats=payload.no_of_seats,
        no_of_days=payload.no_of_days,
        date_of_booking=payload.date_of_booking
    )

    db.add(rental_driver)
    await db.commit()
    await db.refresh(rental_driver)

    return rental_driver
  
@router.put("/{rental_driver_id}/assign")
async def assign_driver_to_rental(
    rental_driver_id: UUID,
    payload: RentalDriverUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if str(current_user.role).upper() != "RENTER":
        raise HTTPException(
            status_code=403,
            detail="Only renters can assign drivers"
        )

    result = await db.execute(
        select(RentalDriver).where(RentalDriver.id == rental_driver_id)
    )
    rental_driver = result.scalar_one_or_none()

    if not rental_driver:
        raise HTTPException(status_code=404, detail="Rental driver request not found")

    if rental_driver.renter_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only assign drivers to your own rental requests"
        )

    rental_driver.driver_id = payload.driver_id

    await db.commit()
    await db.refresh(rental_driver)

    return {
        "success": True,
        "message": "Driver assigned successfully",
        "rental_driver_id": rental_driver.id,
        "driver_id": rental_driver.driver_id,
    }