from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    Form,)
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user_models import User
from app.schemas.Rented_Vehicles import (
    RentedVehicleCreate,
    RentedVehicleUpdate,
    RentedVehicleResponse,
    RentedVehiclePhotoResponse,
    RentedVehicleDocumentResponse,
    RentedVehicleDamageReportResponse,
    RentedVehicleAvailabilityCreate,
    RentedVehicleAvailabilityResponse,
    RentalInspectionCreate,
    RentalInspectionResponse)
from app.services.Rentedvehicleservice import (
    RentedVehicleService,
    VehiclePhotoService,
    VehicleDocumentService,
    VehicleDamageService,
    VehicleAvailabilityService,
    RentalInspectionService)

router = APIRouter(
    prefix="/rented-vehicles",
    tags=["Rented Vehicles"])


@router.post(
    "/",
    response_model=RentedVehicleResponse
)
async def create_vehicle(

    payload: RentedVehicleCreate,

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    return await (
        RentedVehicleService.create_vehicle(
            payload,
            current_user,
            db
        )
    )

@router.get(
    "/my-vehicles",
    response_model=list[RentedVehicleResponse]
)
async def get_my_vehicles(

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    return await (
        RentedVehicleService.get_my_vehicles(
            current_user,
            db
        )
    )


@router.put("/update",
    response_model=RentedVehicleResponse
)
async def update_vehicle(

    payload: RentedVehicleUpdate,

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    return await (
        RentedVehicleService.update_vehicle(
            payload,
            current_user,
            db
        )
    )



@router.delete("/delete")
async def delete_vehicle(

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    return await (
        RentedVehicleService.delete_vehicle(
            current_user,
            db
        )
    )


@router.post(
    "/upload-photos",
    response_model=RentedVehiclePhotoResponse
)
async def upload_vehicle_photo(

    angle: str = Form(...),

    file: UploadFile = File(...),

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    return await (
        VehiclePhotoService.upload_vehicle_photo(
            angle,
            file,
            current_user,
            db
        )
    )


@router.post(
    "/upload-documents",
    response_model=RentedVehicleDocumentResponse
)
async def upload_vehicle_document(


    document_type: str = Form(...),

    file: UploadFile = File(...),

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    return await (
        VehicleDocumentService.upload_document(
            document_type,
            file,
            current_user,
            db
        )
    )


@router.post(
    "/update-damage-report",
    response_model=RentedVehicleDamageReportResponse
)
async def create_damage_report(

    damage_type: str = Form(...),

    description: str = Form(None),

    estimated_repair_cost: float = Form(None),

    damage_photo: UploadFile = File(None),

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    return await (
        VehicleDamageService.create_damage_report(
            damage_type,
            description,
            estimated_repair_cost,
            damage_photo,
            current_user,
            db
        )
    )


@router.post(
    "/update-availability",
    response_model=RentedVehicleAvailabilityResponse
)
async def add_availability(


    payload: RentedVehicleAvailabilityCreate,

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    return await (
        VehicleAvailabilityService.add_availability(
            payload,
            current_user,
            db
        )
    )



@router.post(
    "/inspection",
    response_model=RentalInspectionResponse
)
async def create_inspection(

    payload: RentalInspectionCreate,

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    return await (
        RentalInspectionService.create_inspection(
            payload,
            current_user,
            db
        )
    )

