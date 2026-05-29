from uuid import UUID
from fastapi import ( APIRouter, Depends, HTTPException, status )
from sqlalchemy import ( select )
from sqlalchemy.ext.asyncio import ( AsyncSession )
from app.core.database import ( get_db )
from app.core.security import ( get_current_user )
from app.core.enums import ( DriverStatus, UserRole )
from app.models.user_models import ( User, DriverProfile, KYCDocument )

router = APIRouter( prefix="/admin/drivers", tags=["Admin Drivers"] )

def require_admin( current_user: User ):

    if current_user.role != UserRole.ADMIN:

        raise HTTPException( status_code = status.HTTP_403_FORBIDDEN, detail = "Admin access required" )

@router.get("/")
async def get_all_drivers( db: AsyncSession = Depends(get_db), current_user: User = Depends( get_current_user ) ):

    require_admin(current_user)

    result = await db.execute( select(DriverProfile) )

    drivers = result.scalars().all()

    return drivers

@router.get("/{driver_id}")
async def get_driver( driver_id: UUID, db: AsyncSession = Depends(get_db), current_user: User = Depends( get_current_user )):

    require_admin(current_user)

    result = await db.execute( select(DriverProfile).where( DriverProfile.id == driver_id ) )

    driver = result.scalar_one_or_none()

    if not driver:

        raise HTTPException( status_code=404, detail="Driver not found" )

    kyc_result = await db.execute( select(KYCDocument).where( KYCDocument.user_id == driver.user_id))

    kyc = kyc_result.scalar_one_or_none()

    return { "driver": driver, "kyc_documents": kyc }

@router.put("/{driver_id}/verify")
async def verify_driver( driver_id: UUID, db: AsyncSession = Depends(get_db), current_user: User = Depends( get_current_user )):

    require_admin(current_user)

    result = await db.execute( select(DriverProfile).where( DriverProfile.id == driver_id ))

    driver = result.scalar_one_or_none()

    if not driver:

        raise HTTPException( status_code = 404, detail = "Driver not found" )

    driver.is_verified = True

    driver.status = ( DriverStatus.OFFLINE )

    await db.commit()

    return { "message": "Driver verified successfully" }

@router.put("/{driver_id}/verify-documents")
async def verify_driver_documents(

    driver_id: UUID,

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends( get_current_user )):

    require_admin(current_user)
    
    result = await db.execute( select(DriverProfile).where( DriverProfile.id == driver_id ) )

    driver = result.scalar_one_or_none()

    if not driver:

        raise HTTPException( status_code=404, detail="Driver not found" )
    
    kyc_result = await db.execute( select(KYCDocument).where( KYCDocument.user_id == driver.user_id ) )

    kyc = kyc_result.scalar_one_or_none()

    if not kyc:

        raise HTTPException( status_code=404, detail="KYC documents not found" )
    
    kyc.verification_status = ( "verified" )
    
    driver.is_verified = True

    driver.status = ( DriverStatus.OFFLINE )

    await db.commit()

    return { "message": "Driver documents verified successfully" }

@router.put("/{driver_id}/reject-documents")
async def reject_driver_documents(

    driver_id: UUID,

    reason: str,

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends( get_current_user ) ):

    require_admin(current_user)

    result = await db.execute( select(DriverProfile).where( DriverProfile.id == driver_id ) )

    driver = result.scalar_one_or_none()

    if not driver:

        raise HTTPException( status_code=404, detail="Driver not found" )
    
    kyc_result = await db.execute( select(KYCDocument).where( KYCDocument.user_id == driver.user_id ) )

    kyc = kyc_result.scalar_one_or_none()

    if not kyc:

        raise HTTPException( status_code=404, detail="KYC documents not found" )
    
    kyc.verification_status = ( "rejected" )

    driver.is_verified = False

    driver.status = ( DriverStatus.INACTIVE )

    await db.commit()

    return { "message" : "Driver documents rejected", "reason": reason }

@router.put("/{driver_id}/reject")
async def reject_driver(

    driver_id: UUID,

    reason: str,

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends( get_current_user ) ):

    require_admin(current_user)

    result = await db.execute( select(DriverProfile).where( DriverProfile.id == driver_id ) )

    driver = result.scalar_one_or_none()

    if not driver:

        raise HTTPException( status_code=404, detail="Driver not found" )

    driver.is_verified = False

    driver.status = ( DriverStatus.INACTIVE )

    await db.commit()

    return { "message": "Driver rejected", "reason": reason }

@router.put("/{driver_id}/block")
async def block_driver(

    driver_id: UUID,

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends( get_current_user ) ):

    require_admin(current_user)

    result = await db.execute( select(DriverProfile).where( DriverProfile.id == driver_id ) )

    driver = result.scalar_one_or_none()

    if not driver:

        raise HTTPException( status_code=404, detail="Driver not found" )

    driver.status = ( DriverStatus.BLOCKED )

    await db.commit()

    return { "message": "Driver blocked successfully" }

@router.put("/{driver_id}/unblock")
async def unblock_driver( driver_id: UUID, db: AsyncSession = Depends(get_db), current_user: User = Depends( get_current_user ) ):

    require_admin(current_user)

    result = await db.execute( select(DriverProfile).where( DriverProfile.id == driver_id ) )

    driver = result.scalar_one_or_none()

    if not driver:

        raise HTTPException( status_code=404, detail="Driver not found" )

    driver.status = ( DriverStatus.OFFLINE )

    await db.commit()

    return { "message": "Driver unblocked successfully" }

@router.delete("/{driver_id}")
async def delete_driver( driver_id: UUID, db: AsyncSession = Depends(get_db), current_user: User = Depends( get_current_user ) ):

    require_admin(current_user)

    result = await db.execute( select(DriverProfile).where( DriverProfile.id == driver_id))

    driver = result.scalar_one_or_none()

    if not driver:

        raise HTTPException( status_code = 404, detail = "Driver not found" )

    await db.delete(driver)

    await db.commit()

    return { "message": "Driver deleted successfully" }