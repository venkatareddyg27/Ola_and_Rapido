from uuid import UUID
from fastapi import (APIRouter,Depends,HTTPException)
from sqlalchemy import (select,update)
from sqlalchemy.ext.asyncio import (AsyncSession)
from app.core.database import (get_db)
from app.core.enums import (DriverStatus, UserRole)
from app.core.security import (get_current_user)
from app.models.user_models import (User,DriverProfile,KYCDocument)
from app.models.vehicles import (Vehicle)
from app.schemas.user_schema import (DriverProfileCreate,DriverProfileResponse,DriverDocumentsUpdate)
from app.schemas.vehicle_schema import (VehicleCreate)

router = APIRouter(prefix="/drivercreation",tags=["Drivers"])


def require_driver_role(
    current_user: User):

    if current_user.role != UserRole.DRIVER:

        raise HTTPException(

            status_code=403,

            detail=
            "Only drivers can access this API"
        )

async def get_driver_profile(

    db: AsyncSession,

    user_id: UUID):

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

    if current_user.role == UserRole.ADMIN:

        raise HTTPException(

            status_code=403,

            detail=
            "Admin cannot register as driver"
        )

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

    existing_license = await db.execute(

        select(KYCDocument).where(
            KYCDocument.license_number ==
            payload.license_number
        )
    )

    if existing_license.scalar_one_or_none():

        raise HTTPException(

            status_code=400,

            detail=
            "License already registered"
        )

    existing_aadhaar = await db.execute(

        select(KYCDocument).where(
            KYCDocument.aadhaar_number ==
            payload.aadhaar_number
        )
    )

    if existing_aadhaar.scalar_one_or_none():

        raise HTTPException(

            status_code=400,

            detail=
            "Aadhaar already registered"
        )

    existing_rc = await db.execute(

        select(KYCDocument).where(
            KYCDocument.rc_number ==
            payload.rc_number
        )
    )

    if existing_rc.scalar_one_or_none():

        raise HTTPException(

            status_code=400,

            detail=
            "RC already registered"
        )

    current_user.role = (
        UserRole.DRIVER
    )

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

        # OTHER
        insurance_url=
        payload.insurance_url,

        pollution_certificate_url=
        payload.pollution_certificate_url,

        verification_status=
        "PENDING"
    )

    db.add(kyc)

    try:

        await db.commit()

    except Exception:

        await db.rollback()

        raise

    await db.refresh(driver)

    return driver

@router.put("/documents")
async def upload_driver_documents(

    payload: DriverDocumentsUpdate,

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

        select(KYCDocument).where(
            KYCDocument.user_id ==
            current_user.id
        )
    )

    kyc = result.scalar_one_or_none()

    if not kyc:

        raise HTTPException(

            status_code=404,

            detail=
            "KYC documents not found"
        )

    if payload.license_number:

        existing_license = await db.execute(

            select(KYCDocument).where(

                KYCDocument.license_number ==
                payload.license_number,

                KYCDocument.user_id !=
                current_user.id
            )
        )

        if existing_license.scalar_one_or_none():

            raise HTTPException(

                status_code=400,

                detail=
                "License already exists"
            )

        kyc.license_number = (
            payload.license_number
        )

    if payload.license_front_url:

        kyc.license_front_url = (
            payload.license_front_url
        )

    if payload.license_back_url:

        kyc.license_back_url = (
            payload.license_back_url
        )

    if payload.aadhaar_number:

        existing_aadhaar = await db.execute(

            select(KYCDocument).where(

                KYCDocument.aadhaar_number ==
                payload.aadhaar_number,

                KYCDocument.user_id !=
                current_user.id
            )
        )

        if existing_aadhaar.scalar_one_or_none():

            raise HTTPException(

                status_code=400,

                detail=
                "Aadhaar already exists"
            )

        kyc.aadhaar_number = (
            payload.aadhaar_number
        )

    if payload.aadhaar_front_url:

        kyc.aadhaar_front_url = (
            payload.aadhaar_front_url
        )

    if payload.aadhaar_back_url:

        kyc.aadhaar_back_url = (
            payload.aadhaar_back_url
        )



    if payload.rc_number:

        existing_rc = await db.execute(

            select(KYCDocument).where(

                KYCDocument.rc_number ==
                payload.rc_number,

                KYCDocument.user_id !=
                current_user.id
            )
        )

        if existing_rc.scalar_one_or_none():

            raise HTTPException(

                status_code=400,

                detail=
                "RC already exists"
            )

        kyc.rc_number = (
            payload.rc_number
        )

    if payload.rc_front_url:

        kyc.rc_front_url = (
            payload.rc_front_url
        )

    if payload.rc_back_url:

        kyc.rc_back_url = (
            payload.rc_back_url
        )


    if payload.insurance_url:

        kyc.insurance_url = (
            payload.insurance_url
        )

    if payload.pollution_certificate_url:

        kyc.pollution_certificate_url = (
            payload.pollution_certificate_url
        )


    kyc.verification_status = (
        "PENDING"
    )

    driver.is_verified = False

    try:

        await db.commit()

    except Exception:

        await db.rollback()

        raise

    return {

        "message":
        "Documents uploaded successfully",

        "verification_status":
        "PENDING"
    }


@router.post("/vehicle")
async def add_vehicle(

    payload: VehicleCreate,

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

    if driver.vehicle_id:

        raise HTTPException(

            status_code=400,

            detail=
            "Driver already has vehicle"
        )

    existing_vehicle = await db.execute(

        select(Vehicle).where(
            Vehicle.registration_number ==
            payload.registration_number
        )
    )

    if existing_vehicle.scalar_one_or_none():

        raise HTTPException(

            status_code=400,

            detail=
            "Vehicle already registered"
        )

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

        colour=
        payload.colour
    )

    db.add(vehicle)

    await db.flush()

    driver.vehicle_id = vehicle.id

    try:

        await db.commit()

    except Exception:

        await db.rollback()

        raise

    await db.refresh(vehicle)

    return {

        "message":
        "Vehicle added successfully",

        "vehicle_id":
        str(vehicle.id),

        "registration_number":
        vehicle.registration_number
    }