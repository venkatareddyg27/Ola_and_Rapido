from uuid import UUID
from decimal import Decimal
from datetime import datetime, date
from fastapi import (APIRouter,Depends,HTTPException,Query)
from sqlalchemy import (select,and_,or_,)
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.vehicles import Vehicle
from app.models.rentals import Rental, RentalInspection
from app.models.support import Dispute
from app.schemas.rentals import (
    RentalCreate,
    RentalDisputeRequest,
    RentalInspectionCreate,)
from app.core.enums import (
    RentalStatus,
    DepositStatus,
    DisputeStatus,
    DisputePriority,)

router = APIRouter(
    prefix="/rentals",
    tags=["Rentals"],)


@router.get("/vehicles")
async def browse_rental_vehicles(
    category: str | None = Query(None),
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    max_price: float | None = Query(None),
    db: AsyncSession = Depends(get_db),):
    query = select(Vehicle)

    if category:
        query = query.where(Vehicle.category == category)

    if max_price:
        query = query.where(Vehicle.daily_rate <= max_price)

    result = await db.execute(query)
    vehicles = result.scalars().all()

    available_vehicles = []

    for vehicle in vehicles:

        if start_date and end_date:

            overlap_query = await db.execute(
                select(Rental).where(
                    and_(
                        Rental.vehicle_id == vehicle.id,
                        Rental.status.in_(
                            [
                                RentalStatus.BOOKED,
                                RentalStatus.ACTIVE,
                            ]
                        ),
                        or_(
                            and_(
                                Rental.pickup_time <= datetime.combine(
                                    start_date,
                                    datetime.max.time(),
                                ),
                                Rental.drop_time >= datetime.combine(
                                    start_date,
                                    datetime.min.time(),
                                ),
                            ),
                            and_(
                                Rental.pickup_time <= datetime.combine(
                                    end_date,
                                    datetime.max.time(),
                                ),
                                Rental.drop_time >= datetime.combine(
                                    end_date,
                                    datetime.min.time(),
                                ),
                            ),
                        ),
                    )
                )
            )

            booking = overlap_query.scalar_one_or_none()

            if booking:
                continue

        available_vehicles.append(vehicle)

    return {
        "success": True,
        "count": len(available_vehicles),
        "items": available_vehicles,
    }


@router.post("/book")
async def book_rental_vehicle(
    payload: RentalCreate,
    db: AsyncSession = Depends(get_db),
):
    if payload.start_date >= payload.end_date:
        raise HTTPException(
            status_code=400,
            detail="End date must be greater than start date",
        )

    if payload.start_date < date.today():
        raise HTTPException(
            status_code=400,
            detail="Start date cannot be in past",
        )

    vehicle_query = await db.execute(
        select(Vehicle).where(
            Vehicle.id == payload.vehicle_id
        )
    )

    vehicle = vehicle_query.scalar_one_or_none()

    if not vehicle:
        raise HTTPException(
            status_code=404,
            detail="Vehicle not found",
        )

    overlap_query = await db.execute(
        select(Rental).where(
            and_(
                Rental.vehicle_id == payload.vehicle_id,
                Rental.status.in_(
                    [
                        RentalStatus.BOOKED,
                        RentalStatus.ACTIVE,
                    ]
                ),
                or_(
                    and_(
                        Rental.pickup_time <= datetime.combine(
                            payload.start_date,
                            datetime.max.time(),
                        ),
                        Rental.drop_time >= datetime.combine(
                            payload.start_date,
                            datetime.min.time(),
                        ),
                    ),
                    and_(
                        Rental.pickup_time <= datetime.combine(
                            payload.end_date,
                            datetime.max.time(),
                        ),
                        Rental.drop_time >= datetime.combine(
                            payload.end_date,
                            datetime.min.time(),
                        ),
                    ),
                ),
            )
        )
    )

    existing_booking = overlap_query.scalar_one_or_none()

    if existing_booking:
        raise HTTPException(
            status_code=400,
            detail="Vehicle already booked for selected dates",
        )

    total_days = (
        payload.end_date - payload.start_date
    ).days

    daily_rate = Decimal(str(vehicle.daily_rate))

    total_fare = daily_rate * total_days

    deposit_amount = Decimal("5000.00")

    rental = Rental(
        vehicle_id=vehicle.id,
        renter_id=payload.renter_id,
        owner_id=payload.owner_id or vehicle.owner_id,
        pickup_time=datetime.combine(
            payload.start_date,
            datetime.min.time(),
        ),
        drop_time=datetime.combine(
            payload.end_date,
            datetime.min.time(),
        ),
        daily_rate=daily_rate,
        total_fare=total_fare,
        deposit_amount=deposit_amount,
        status=RentalStatus.BOOKED,
        deposit_status=DepositStatus.PENDING,
    )

    db.add(rental)

    await db.commit()
    await db.refresh(rental)

    return {
        "success": True,
        "message": "Vehicle booked successfully",
        "rental_id": rental.id,
        "vehicle_id": vehicle.id,
        "total_days": total_days,
        "daily_rate": daily_rate,
        "total_fare": total_fare,
        "deposit_amount": deposit_amount,
        "status": rental.status,
    }


@router.get("/{rental_id}")
async def get_rental_details(
    rental_id: UUID,
    db: AsyncSession = Depends(get_db),):
    rental_query = await db.execute(
        select(Rental).where(
            Rental.id == rental_id
        )
    )

    rental = rental_query.scalar_one_or_none()

    if not rental:
        raise HTTPException(
            status_code=404,
            detail="Rental not found",
        )

    return {
        "success": True,
        "item": rental,
    }


@router.get("/customer/{customer_id}")
async def customer_rental_history(
    customer_id: UUID,
    db: AsyncSession = Depends(get_db),):
    result = await db.execute(
        select(Rental).where(
            Rental.renter_id == customer_id
        )
    )

    rentals = result.scalars().all()

    return {
        "success": True,
        "count": len(rentals),
        "items": rentals,
    }


@router.put("/{rental_id}/start")
async def start_rental(
    rental_id: UUID,
    db: AsyncSession = Depends(get_db),):
    rental_query = await db.execute(
        select(Rental).where(
            Rental.id == rental_id
        )
    )

    rental = rental_query.scalar_one_or_none()

    if not rental:
        raise HTTPException(
            status_code=404,
            detail="Rental not found",
        )

    if rental.status != RentalStatus.BOOKED:
        raise HTTPException(
            status_code=400,
            detail="Rental cannot be started",
        )

    rental.status = RentalStatus.ACTIVE

    await db.commit()
    await db.refresh(rental)

    return {
        "success": True,
        "message": "Rental started successfully",
        "status": rental.status,
    }

@router.put("/{rental_id}/complete")
async def complete_rental(
    rental_id: UUID,
    db: AsyncSession = Depends(get_db),):
    rental_query = await db.execute(
        select(Rental).where(
            Rental.id == rental_id
        )
    )

    rental = rental_query.scalar_one_or_none()

    if not rental:
        raise HTTPException(
            status_code=404,
            detail="Rental not found",
        )

    if rental.status != RentalStatus.ACTIVE:
        raise HTTPException(
            status_code=400,
            detail="Only active rental can be completed",
        )

    rental.status = RentalStatus.COMPLETED
    rental.deposit_status = DepositStatus.REFUNDED

    await db.commit()
    await db.refresh(rental)

    return {
        "success": True,
        "message": "Rental completed successfully",
        "deposit_refunded": True,
        "status": rental.status,
    }



@router.put("/{rental_id}/cancel")
async def cancel_rental(
    rental_id: UUID,
    db: AsyncSession = Depends(get_db),):
    rental_query = await db.execute(
        select(Rental).where(
            Rental.id == rental_id
        )
    )

    rental = rental_query.scalar_one_or_none()

    if not rental:
        raise HTTPException(
            status_code=404,
            detail="Rental not found",
        )

    if rental.status in [
        RentalStatus.COMPLETED,
        RentalStatus.CANCELLED,
    ]:
        raise HTTPException(
            status_code=400,
            detail="Rental cannot be cancelled",
        )

    rental.status = RentalStatus.CANCELLED

    await db.commit()
    await db.refresh(rental)

    return {
        "success": True,
        "message": "Rental cancelled successfully",
        "status": rental.status,
    }


@router.post("/{rental_id}/inspection")
async def submit_rental_inspection(
    rental_id: UUID,
    payload: RentalInspectionCreate,
    db: AsyncSession = Depends(get_db),):
    rental_query = await db.execute(
        select(Rental).where(
            Rental.id == rental_id
        )
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
        inspected_at=payload.inspected_at
        or datetime.utcnow(),
        inspector_user_id=payload.inspector_user_id
        or rental.owner_id,
    )

    db.add(inspection)

    await db.commit()
    await db.refresh(inspection)

    return {
        "success": True,
        "message": "Inspection submitted successfully",
        "inspection_id": inspection.id,
    }



@router.post("/{rental_id}/dispute")
async def raise_rental_dispute(
    rental_id: UUID,
    payload: RentalDisputeRequest,
    db: AsyncSession = Depends(get_db),):
    rental_query = await db.execute(
        select(Rental).where(
            Rental.id == rental_id
        )
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