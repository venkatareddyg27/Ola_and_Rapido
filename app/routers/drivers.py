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
    func
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

from app.core.enums import (
    DriverStatus,
    TripStatus,
    UserRole
)

from app.core.security import get_current_user

from app.models.user_models import (
    User,
    DriverProfile,
    DriverLocation,
    KYCDocument
)

from app.models.trips import Trip

from app.models.vehicles import Vehicle

from app.schemas.user_schema import (
    DriverProfileCreate,
    DriverProfileResponse
)

from app.schemas.vehicle_schema import (
    VehicleCreate
)

router = APIRouter(
    prefix="/drivers",
    tags=["Drivers"]
)

# =========================================================
# CHECK DRIVER ROLE
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
# REGISTER DRIVER
# =========================================================

@router.post(
    "/register",
    response_model=DriverProfileResponse
)
async def register_driver(

    payload: DriverProfileCreate,

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    # =====================================================
    # CHECK ROLE
    # =====================================================

    if current_user.role == UserRole.ADMIN:

        raise HTTPException(

            status_code=403,

            detail=
            "Admin cannot register as driver"
        )

    # CONVERT CUSTOMER TO DRIVER

    current_user.role = (
        UserRole.DRIVER
    )

    # =====================================================
    # CHECK EXISTING DRIVER
    # =====================================================

    existing_driver = await db.execute(

        select(DriverProfile).where(
            DriverProfile.user_id ==
            current_user.id
        )
    )

    if existing_driver.scalar_one_or_none():

        raise HTTPException(

            status_code=400,

            detail=
            "Driver already registered"
        )

    # =====================================================
    # CREATE DRIVER PROFILE
    # =====================================================

    driver = DriverProfile(

        user_id=current_user.id,

        subscription_plan=
        payload.subscription_plan,

        bank_account_number=
        payload.bank_account_number,

        ifsc_code=
        payload.ifsc_code,

        upi_id=
        payload.upi_id,

        selfie_url=
        payload.selfie_url,

        status=
        DriverStatus.OFFLINE,

        rating=5.0,

        total_trips=0,

        commission_rate=10,

        is_verified=False
    )

    db.add(driver)

    await db.flush()

    # =====================================================
    # SAVE KYC DOCUMENTS
    # =====================================================

    kyc = KYCDocument(

        user_id=current_user.id,

        # LICENSE
        license_number=
        payload.license_number,

        license_front_url=
        payload.license_front_url,

        license_back_url=
        payload.license_back_url,

        # AADHAAR
        aadhaar_number=
        payload.aadhaar_number,

        aadhaar_front_url=
        payload.aadhaar_front_url,

        aadhaar_back_url=
        payload.aadhaar_back_url,

        # RC
        rc_number=
        payload.rc_number,

        rc_front_url=
        payload.rc_front_url,

        rc_back_url=
        payload.rc_back_url,

        # OTHER DOCS
        insurance_url=
        payload.insurance_url,

        pollution_certificate_url=
        payload.pollution_certificate_url,

        verification_status=
        "PENDING"
    )

    db.add(kyc)

    await db.commit()

    await db.refresh(driver)

    return driver

# =========================================================
# ADD VEHICLE
# =========================================================

@router.post("/vehicle")
async def add_vehicle(

    payload: VehicleCreate,

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    # =====================================================
    # CHECK ROLE
    # =====================================================

    require_driver_role(current_user)

    # =====================================================
    # GET DRIVER PROFILE
    # =====================================================

    driver_result = await db.execute(

        select(DriverProfile).where(
            DriverProfile.user_id ==
            current_user.id
        )
    )

    driver = driver_result.scalar_one_or_none()

    if not driver:

        raise HTTPException(

            status_code=404,

            detail=
            "Driver profile not found"
        )

    # =====================================================
    # CREATE VEHICLE
    # =====================================================

    vehicle = Vehicle(

        owner_id=current_user.id,

        make=payload.make,

        model=payload.model,

        year=payload.year,

        registration_number=
        payload.registration_number,

        category=payload.category,

        sitting_capacity=
        payload.sitting_capacity,

        fuel_type=
        payload.fuel_type,

        colour=payload.colour
    )

    db.add(vehicle)

    await db.flush()

    # LINK VEHICLE

    driver.vehicle_id = vehicle.id

    await db.commit()

    return {

        "message":
        "Vehicle added successfully",

        "vehicle_id":
        str(vehicle.id)
    }

# =========================================================
# GO ONLINE/OFFLINE
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

    result = await db.execute(

        select(DriverProfile).where(
            DriverProfile.user_id ==
            current_user.id
        )
    )

    driver = result.scalar_one_or_none()

    if not driver:

        raise HTTPException(

            status_code=404,

            detail="Driver not found"
        )

    # DRIVER MUST BE VERIFIED

    if not driver.is_verified:

        raise HTTPException(

            status_code=400,

            detail=
            "Admin approval pending"
        )

    # BLOCKED DRIVER CHECK

    if driver.status == DriverStatus.BLOCKED:

        raise HTTPException(

            status_code=403,

            detail=
            "Driver account blocked"
        )

    driver.status = status

    # SAVE LOCATION

    location = DriverLocation(

        driver_id=driver.id,

        latitude=latitude,

        longitude=longitude,

        heading=heading,

        speed=speed,

        is_active=True
    )

    db.add(location)

    await db.commit()

    return {

        "message":
        "Driver status updated"
    }

# =========================================================
# ACCEPT RIDE
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

    # GET DRIVER

    driver_result = await db.execute(

        select(DriverProfile).where(
            DriverProfile.user_id ==
            current_user.id
        )
    )

    driver = driver_result.scalar_one_or_none()

    if not driver:

        raise HTTPException(

            status_code=404,

            detail="Driver not found"
        )

    # GET TRIP

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

    # ASSIGN DRIVER

    trip.driver_id = driver.id

    trip.status = (
        TripStatus.DRIVER_ASSIGNED
    )

    driver.status = (
        DriverStatus.ON_TRIP
    )

    await db.commit()

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

    trip.status = (
        TripStatus.DRIVER_ARRIVED
    )

    await db.commit()

    return {

        "message":
        "Driver reached pickup"
    }

# =========================================================
# START RIDE WITH OTP
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
# COMPLETE RIDE
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

    # GET DRIVER

    driver_result = await db.execute(

        select(DriverProfile).where(
            DriverProfile.user_id ==
            current_user.id
        )
    )

    driver = driver_result.scalar_one_or_none()

    if not driver:

        raise HTTPException(

            status_code=404,

            detail="Driver not found"
        )

    # GET TRIP

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

    # COMPLETE TRIP

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
# CANCEL RIDE
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

    trip.status = (
        TripStatus.CANCELLED
    )

    trip.cancel_reason = reason

    await db.commit()

    return {

        "message":
        "Ride cancelled"
    }

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

    # GET DRIVER

    driver_result = await db.execute(

        select(DriverProfile).where(
            DriverProfile.user_id ==
            current_user.id
        )
    )

    driver = driver_result.scalar_one_or_none()

    if not driver:

        raise HTTPException(

            status_code=404,

            detail="Driver not found"
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
        earnings or 0,

        "rides_completed":
        rides or 0
    }