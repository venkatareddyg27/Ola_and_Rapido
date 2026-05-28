from datetime import datetime
from uuid import UUID
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.core.enums import (VehicleCategory,VehicleStatus,VehiclePhotoAngle)


class VehicleBase(BaseModel):
    driver_id: UUID
    make: str
    model: str
    year: int
    registration_number: str
    category: VehicleCategory
    sitting_capacity: Optional[int] = None
    fuel_type: Optional[str] = None
    colour: Optional[str] = None
    daily_rate:float


class VehicleCreate(VehicleBase):
    pass


class VehicleUpdate(BaseModel):
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    category: Optional[VehicleCategory] = None
    sitting_capacity: Optional[int] = None
    fuel_type: Optional[str] = None
    colour: Optional[str] = None
    status: Optional[VehicleStatus] = None

class VehicleUpdateStatus(BaseModel):

    status: str



class VehicleDocumentResponse(BaseModel):

    id: UUID
    vehicle_id: UUID
    document_type: str
    document_url: str
    verification_status: str
    created_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True)


class VehicleResponse(BaseModel):
    id: UUID
    owner_id: UUID
    make: str | None = None
    model: str
    year: int
    registration_number: str
    category: VehicleCategory
    status: VehicleStatus
    sitting_capacity: int
    fuel_type: str | None = None
    colour: str
    daily_rate: float

    model_config = ConfigDict(from_attributes=True)


class VehiclePhotoBase(BaseModel):
    vehicle_id: UUID
    photo_url: str
    angle: VehiclePhotoAngle


class VehiclePhotoCreate(VehiclePhotoBase):
    pass



class VehiclePhotoUpdate(BaseModel):
    photo_url: Optional[str] = None
    angle: Optional[VehiclePhotoAngle] = None


class VehiclePhotoResponse(VehiclePhotoBase):
    id: UUID
    uploaded_at: datetime

    class Config:
        from_attributes = True