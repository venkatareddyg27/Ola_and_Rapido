from uuid import UUID
from fastapi import (APIRouter,Depends,HTTPException,UploadFile,File,Form)
from sqlalchemy import (select)
from sqlalchemy.ext.asyncio import (AsyncSession)
from app.core.database import get_db
from app.models.user_models import (User,DriverProfile)
from app.models.vehicles import (Vehicle,VehicleDocument)
from app.schemas.vehicle_schema import (VehicleCreate,VehicleResponse,VehicleUpdateStatus,VehicleDocumentResponse,VehicleBase)
from app.core.security import (get_current_user)
from app.core.enums import VehicleStatus

router = APIRouter(
    prefix="/vehicles",
    tags=["Vehicles"])


@router.post(
    "/register",
    response_model=VehicleResponse)
async def register_vehicle(
    payload: VehicleCreate,

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):
    """
    Register vehicle for driver.
    """


    result = await db.execute(
        select(DriverProfile).where(
            DriverProfile.user_id ==
            current_user.id
        )
    )

    driver_profile = (
        result.scalars().first()
    )

    if not driver_profile:

        raise HTTPException(
            status_code=404,
            detail="Driver profile not found"
        )

    vehicle = Vehicle(
        owner_id=driver_profile.user_id,
        make=payload.make,
        model=payload.model,
        year=payload.year,
        registration_number=payload.registration_number,
        category=payload.category,
        status=VehicleStatus.ACTIVE,
        sitting_capacity=payload.sitting_capacity,
        fuel_type=payload.fuel_type,
        colour=payload.colour,
        daily_rate=payload.daily_rate   # REQUIRED
    )

    db.add(vehicle)

    await db.commit()

    await db.refresh(vehicle)


    driver_profile.vehicle_id = (
        vehicle.id
    )

    await db.commit()

    return vehicle

@router.get(
    "/my-vehicles",
    response_model=list[VehicleResponse]
)
async def my_vehicles(
    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):
    """
    Get driver vehicles.
    """

    result = await db.execute(
        select(DriverProfile).where(
            DriverProfile.user_id ==
            current_user.id
        )
    )

    driver_profile = (
        result.scalars().first()
    )

    if not driver_profile:

        raise HTTPException(
            status_code=404,
            detail="Driver profile not found"
        )


    vehicles_result = await db.execute(
        select(Vehicle).where(
            Vehicle.owner_id ==
            current_user.id
        )
    )

    vehicles = (
        vehicles_result.scalars().all()
    )

    return vehicles

@router.get(
    "/{vehicle_id}",
    response_model=VehicleResponse
)
async def get_vehicle(
    vehicle_id: UUID,

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):
    """
    Get detailed vehicle info.
    """

    result = await db.execute(
        select(Vehicle).where(
            Vehicle.id == vehicle_id
        )
    )

    vehicle = (
        result.scalars().first()
    )

    if not vehicle:

        raise HTTPException(
            status_code=404,
            detail="Vehicle not found"
        )

    return vehicle


@router.put("/{vehicle_id}/status")
async def update_vehicle_status(
    vehicle_id: UUID,

    payload: VehicleUpdateStatus,

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):
    """
    Update vehicle status.
    """

    result = await db.execute(
        select(Vehicle).where(
            Vehicle.id == vehicle_id
        )
    )

    vehicle = (
        result.scalars().first()
    )

    if not vehicle:

        raise HTTPException(
            status_code=404,
            detail="Vehicle not found"
        )

    vehicle.status = payload.status

    await db.commit()

    return {
        "message":
        "Vehicle status updated"
    }

@router.post(
    "/{vehicle_id}/documents",
    response_model=VehicleDocumentResponse
)
async def upload_vehicle_document(
    vehicle_id: UUID,

    document_type: str = Form(...),

    file: UploadFile = File(...),

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):
    """
    Upload vehicle document.
    """

    result = await db.execute(
        select(Vehicle).where(
            Vehicle.id == vehicle_id
        )
    )

    vehicle = (
        result.scalars().first()
    )

    if not vehicle:

        raise HTTPException(
            status_code=404,
            detail="Vehicle not found"
        )

    file_url = (
        f"/uploads/vehicles/"
        f"{file.filename}"
    )

    document = VehicleDocument(

        vehicle_id=vehicle.id,

        document_type=
        document_type,

        document_url=file_url,

        verification_status=
        "pending"
    )

    db.add(document)

    await db.commit()

    await db.refresh(document)

    return document