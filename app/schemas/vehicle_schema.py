
from datetime import datetime
from uuid import UUID
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.core.enums import (
    VehicleCategory,
    VehicleStatus,
    VehiclePhotoAngle
)


# =========================================================
# VEHICLE BASE
# =========================================================

class VehicleBase(BaseModel):
    driver_id: UUID
    make: str
    model: str
    year: int

    vehicle_number: str

    category: VehicleCategory

    sitting_capacity: Optional[int] = None

    fuel_type: Optional[str] = None

    colour: Optional[str] = None


# =========================================================
# CREATE VEHICLE
# =========================================================

class VehicleCreate(VehicleBase):
    pass


# =========================================================
# UPDATE VEHICLE
# =========================================================

class VehicleUpdate(BaseModel):
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None

    category: Optional[VehicleCategory] = None

    sitting_capacity: Optional[int] = None

    fuel_type: Optional[str] = None

    colour: Optional[str] = None

    status: Optional[VehicleStatus] = None

class VehicleUpdateStatus(
    BaseModel
):

    status: str


# =========================================================
# VEHICLE DOCUMENT RESPONSE
# =========================================================

class VehicleDocumentResponse(
    BaseModel
):

    id: UUID

    vehicle_id: UUID

    document_type: str

    document_url: str

    verification_status: str

    created_at: Optional[
        datetime
    ] = None

    model_config = ConfigDict(
        from_attributes=True
    )
# =========================================================
# VEHICLE RESPONSE
# =========================================================

class VehicleResponse(VehicleBase):
    id: UUID

    status: VehicleStatus

    created_at: datetime

    class Config:
        from_attributes = True


# =========================================================
# VEHICLE PHOTO BASE
# =========================================================

class VehiclePhotoBase(BaseModel):
    vehicle_id: UUID

    photo_url: str

    angle: VehiclePhotoAngle


# =========================================================
# CREATE VEHICLE PHOTO
# =========================================================

class VehiclePhotoCreate(VehiclePhotoBase):
    pass


# =========================================================
# UPDATE VEHICLE PHOTO
# =========================================================

class VehiclePhotoUpdate(BaseModel):
    photo_url: Optional[str] = None

    angle: Optional[VehiclePhotoAngle] = None


# =========================================================
# VEHICLE PHOTO RESPONSE
# =========================================================

class VehiclePhotoResponse(VehiclePhotoBase):
    id: UUID

    uploaded_at: datetime

    class Config:
        from_attributes = True