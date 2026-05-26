from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy import (
    select
)

from sqlalchemy.orm import (
    selectinload
)

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.core.database import (
    get_db
)

from app.core.security import (
    get_current_user
)

from app.core.enums import (
    DriverStatus,
    UserRole
)

from app.models.user_models import (
    User,
    DriverProfile,
    KYCDocument
)


router = APIRouter(

    prefix="/admin/drivers",

    tags=["Admin Drivers"]

)


# =========================================================
# ADMIN VALIDATION
# =========================================================

def require_admin(
    current_user: User
):

    if current_user.role != UserRole.ADMIN:

        raise HTTPException(

            status_code=
            status.HTTP_403_FORBIDDEN,

            detail=
            "Admin access required"

        )


# =========================================================
# GET ALL DRIVERS
# =========================================================

@router.get("/")
async def get_all_drivers(

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )

):

    require_admin(current_user)

    result = await db.execute(

        select(DriverProfile)

        .options(

            selectinload(
                DriverProfile.user
            )

        )

    )

    drivers = result.scalars().all()

    response = []

    for driver in drivers:

        response.append({

            "driver_id": driver.id,

            "driver_name": (

                driver.user.full_name

                if driver.user

                else None

            ),

            "email": (

                driver.user.email

                if driver.user

                else None

            ),

            "phone_number": (

                driver.user.mobile_number

                if driver.user

                else None

            ),

            "status": driver.status,

            "is_verified": (
                driver.is_verified
            )

        })

    return response


# =========================================================
# GET SINGLE DRIVER
# =========================================================

@router.get("/{driver_id}")
async def get_driver(

    driver_id: UUID,

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )

):

    require_admin(current_user)

    result = await db.execute(

        select(DriverProfile)

        .options(

            selectinload(
                DriverProfile.user
            )

        )

        .where(
            DriverProfile.id == driver_id
        )

    )

    driver = result.scalars().first()

    if not driver:

        raise HTTPException(

            status_code=404,

            detail="Driver not found"

        )

    # =====================================================
    # GET KYC DOCUMENTS
    # =====================================================

    kyc_result = await db.execute(

        select(KYCDocument)

        .where(
            KYCDocument.user_id ==
            driver.user_id
        )

    )

    kyc = kyc_result.scalars().first()

    return {

        "driver_id": driver.id,

        "driver_name": (

            driver.user.full_name

            if driver.user

            else None

        ),

        "email": (

            driver.user.email

            if driver.user

            else None

        ),

        "phone_number": (

            driver.user.mobile_number

            if driver.user

            else None

        ),

        "status": driver.status,

        "is_verified": (
            driver.is_verified
        ),

        "kyc_documents": kyc

    }


# =========================================================
# GET DRIVER DOCUMENTS
# =========================================================

@router.get("/{driver_id}/documents")
async def get_driver_documents(

    driver_id: UUID,

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )

):

    require_admin(current_user)

    # =====================================================
    # GET DRIVER
    # =====================================================

    result = await db.execute(

        select(DriverProfile)

        .options(

            selectinload(
                DriverProfile.user
            )

        )

        .where(
            DriverProfile.id == driver_id
        )

    )

    driver = result.scalars().first()

    # =====================================================
    # DRIVER NOT FOUND
    # =====================================================

    if not driver:

        raise HTTPException(

            status_code=404,

            detail="Driver not found"

        )

    # =====================================================
    # GET KYC DOCUMENTS
    # =====================================================

    kyc_result = await db.execute(

        select(KYCDocument)

        .where(
            KYCDocument.user_id
            == driver.user_id
        )

    )

    kyc = kyc_result.scalars().first()

    # =====================================================
    # DOCUMENTS NOT FOUND
    # =====================================================

    if not kyc:

        raise HTTPException(

            status_code=404,

            detail="KYC documents not found"

        )

    # =====================================================
    # RESPONSE
    # =====================================================

    return {

        "driver_id": driver.id,

        "driver_name": (

            driver.user.full_name

            if driver.user

            else None

        ),

        "email": (

            driver.user.email

            if driver.user

            else None

        ),

        "phone_number": (

            driver.user.mobile_number

            if driver.user

            else None

        ),

        "is_verified": (
            driver.is_verified
        ),

        "driver_status": (
            driver.status
        ),

        # =================================================
        # DOCUMENTS
        # =================================================

        "aadhaar_number": (
            kyc.aadhaar_number
        ),

        "pan_number": (
            kyc.pan_number
        ),

        "driving_license_number": (
            kyc.license_number
        ),

        "aadhaar_front_image": (
            kyc.aadhaar_front_url
        ),

        "aadhaar_back_image": (
            kyc.aadhaar_back_url
        ),

        "pan_card_image": (
            kyc.pan_front_url
        ),

        "driving_license_image": (
            kyc.license_front_url
        ),

        "verification_status": (
            kyc.verification_status
        ),

        "submitted_at": (
            kyc.created_at
        )

    }


# =========================================================
# VERIFY DRIVER
# =========================================================

@router.put("/{driver_id}/verify")
async def verify_driver(

    driver_id: UUID,

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )

):

    require_admin(current_user)

    result = await db.execute(

        select(DriverProfile)

        .where(
            DriverProfile.id == driver_id
        )

    )

    driver = result.scalars().first()

    if not driver:

        raise HTTPException(

            status_code=404,

            detail="Driver not found"

        )

    driver.is_verified = True

    driver.status = (
        DriverStatus.OFFLINE
    )

    await db.commit()

    return {

        "message":
        "Driver verified successfully"

    }


# =========================================================
# VERIFY DRIVER DOCUMENTS
# =========================================================

@router.put("/{driver_id}/verify-documents")
async def verify_driver_documents(

    driver_id: UUID,

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )

):

    require_admin(current_user)

    # =====================================================
    # GET DRIVER
    # =====================================================

    result = await db.execute(

        select(DriverProfile)

        .where(
            DriverProfile.id == driver_id
        )

    )

    driver = result.scalars().first()

    if not driver:

        raise HTTPException(

            status_code=404,

            detail="Driver not found"

        )

    # =====================================================
    # GET KYC DOCUMENTS
    # =====================================================

    kyc_result = await db.execute(

        select(KYCDocument)

        .where(
            KYCDocument.user_id ==
            driver.user_id
        )

    )

    kyc = kyc_result.scalars().first()

    if not kyc:

        raise HTTPException(

            status_code=404,

            detail="KYC documents not found"

        )

    # =====================================================
    # VERIFY DOCUMENTS
    # =====================================================

    kyc.verification_status = (
        "verified"
    )

    driver.is_verified = True

    driver.status = (
        DriverStatus.OFFLINE
    )

    await db.commit()

    return {

        "message":
        "Driver documents verified successfully"

    }


# =========================================================
# REJECT DRIVER DOCUMENTS
# =========================================================

@router.put("/{driver_id}/reject-documents")
async def reject_driver_documents(

    driver_id: UUID,

    reason: str,

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )

):

    require_admin(current_user)

    result = await db.execute(

        select(DriverProfile)

        .where(
            DriverProfile.id == driver_id
        )

    )

    driver = result.scalars().first()

    if not driver:

        raise HTTPException(

            status_code=404,

            detail="Driver not found"

        )

    kyc_result = await db.execute(

        select(KYCDocument)

        .where(
            KYCDocument.user_id ==
            driver.user_id
        )

    )

    kyc = kyc_result.scalars().first()

    if not kyc:

        raise HTTPException(

            status_code=404,

            detail="KYC documents not found"

        )

    kyc.verification_status = (
        "rejected"
    )

    driver.is_verified = False

    driver.status = (
        DriverStatus.INACTIVE
    )

    await db.commit()

    return {

        "message":
        "Driver documents rejected",

        "reason":
        reason

    }


# =========================================================
# REJECT DRIVER
# =========================================================

@router.put("/{driver_id}/reject")
async def reject_driver(

    driver_id: UUID,

    reason: str,

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )

):

    require_admin(current_user)

    result = await db.execute(

        select(DriverProfile)

        .where(
            DriverProfile.id == driver_id
        )

    )

    driver = result.scalars().first()

    if not driver:

        raise HTTPException(

            status_code=404,

            detail="Driver not found"

        )

    driver.is_verified = False

    driver.status = (
        DriverStatus.INACTIVE
    )

    await db.commit()

    return {

        "message":
        "Driver rejected",

        "reason":
        reason

    }


# =========================================================
# BLOCK DRIVER
# =========================================================

@router.put("/{driver_id}/block")
async def block_driver(

    driver_id: UUID,

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )

):

    require_admin(current_user)

    result = await db.execute(

        select(DriverProfile)

        .where(
            DriverProfile.id == driver_id
        )

    )

    driver = result.scalars().first()

    if not driver:

        raise HTTPException(

            status_code=404,

            detail="Driver not found"

        )

    driver.status = (
        DriverStatus.BLOCKED
    )

    await db.commit()

    return {

        "message":
        "Driver blocked successfully"

    }


# =========================================================
# UNBLOCK DRIVER
# =========================================================

@router.put("/{driver_id}/unblock")
async def unblock_driver(

    driver_id: UUID,

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )

):

    require_admin(current_user)

    result = await db.execute(

        select(DriverProfile)

        .where(
            DriverProfile.id == driver_id
        )

    )

    driver = result.scalars().first()

    if not driver:

        raise HTTPException(

            status_code=404,

            detail="Driver not found"

        )

    driver.status = (
        DriverStatus.OFFLINE
    )

    await db.commit()

    return {

        "message":
        "Driver unblocked successfully"

    }


# =========================================================
# DELETE DRIVER
# =========================================================

@router.delete("/{driver_id}")
async def delete_driver(

    driver_id: UUID,

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )

):

    require_admin(current_user)

    result = await db.execute(

        select(DriverProfile)

        .where(
            DriverProfile.id == driver_id
        )

    )

    driver = result.scalars().first()

    if not driver:

        raise HTTPException(

            status_code=404,

            detail="Driver not found"

        )

    await db.delete(driver)

    await db.commit()

    return {

        "message":
        "Driver deleted successfully"

    }