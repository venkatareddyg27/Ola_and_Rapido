from uuid import UUID
from fastapi import (APIRouter,Depends,HTTPException,UploadFile,File,Form)
from sqlalchemy import (select)
from sqlalchemy.ext.asyncio import (AsyncSession)
from app.core.database import get_db
from app.models.user_models import (User,DriverProfile)
from app.models.vehicles import (Vehicle,VehicleDocument)
from app.schemas.vehicle_schema import (VehicleCreate,VehicleResponse,VehicleUpdateStatus,VehicleDocumentResponse)
from app.core.security import (get_current_user)

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

        driver_id=driver_profile.id,

        category=payload.category,

        brand=payload.brand,

        model=payload.model,

        vehicle_number=
        payload.vehicle_number,

        color=payload.color,

        manufacturing_year=
        payload.manufacturing_year,

        seating_capacity=
        payload.seating_capacity,

        status="active"
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
            Vehicle.driver_id ==
            driver_profile.id
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