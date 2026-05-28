from uuid import UUID
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field
from typing import Optional, List
from app.core.enums import (VehicleCategory,VehicleStatus,InspectionType,VehiclePhotoAngle)

class RentedVehiclePhotoBase(BaseModel):

    angle: VehiclePhotoAngle


class RentedVehiclePhotoResponse(RentedVehiclePhotoBase):

    id: UUID

    vehicle_id: UUID

    photo_url: str

    uploaded_at: datetime

    class Config:
        from_attributes = True



class RentedVehicleDocumentBase(BaseModel):

    document_type: str


class RentedVehicleDocumentCreate(RentedVehicleDocumentBase):

    expiry_date: Optional[datetime] = None


class RentedVehicleDocumentResponse(RentedVehicleDocumentBase):

    id: UUID

    vehicle_id: UUID

    document_url: str

    verification_status: str

    expiry_date: Optional[datetime]

    created_at: datetime

    class Config:
        from_attributes = True



class RentedVehicleBase(BaseModel):

    make: str

    model: str

    year: int

    registration_number: str

    category: VehicleCategory

    colour: Optional[str] = None

    sitting_capacity: Optional[int] = None

    fuel_type: Optional[str] = None

    transmission_type: Optional[str] = None

    fuel_capacity: Optional[float] = None

    mileage: Optional[float] = None

    current_odometer: Optional[int] = 0

    price_per_hour: Optional[float] = None

    price_per_day: Optional[float] = None

    security_deposit: Optional[float] = None

    ac_available: Optional[bool] = True

    gps_enabled: Optional[bool] = False

    bluetooth_available: Optional[bool] = False

    music_system: Optional[bool] = False

    sunroof: Optional[bool] = False

    airbags: Optional[int] = 2

    boot_space: Optional[str] = None

    city: Optional[str] = None

    state: Optional[str] = None


class RentedVehicleCreate(RentedVehicleBase):
    pass


class RentedVehicleUpdate(BaseModel):

    make: Optional[str] = None

    model: Optional[str] = None

    year: Optional[int] = None

    colour: Optional[str] = None

    price_per_hour: Optional[float] = None

    price_per_day: Optional[float] = None

    is_available: Optional[bool] = None

    status: Optional[VehicleStatus] = None


class RentedVehicleResponse(RentedVehicleBase):

    id: UUID

    owner_id: UUID

    status: VehicleStatus

    is_verified: bool

    has_damage: bool

    created_at: datetime

    updated_at: datetime

    photos: List[RentedVehiclePhotoResponse] = []

    documents: List[RentedVehicleDocumentResponse] = []

    class Config:
        from_attributes = True


class RentalInspectionBase(BaseModel):

    inspection_type: InspectionType

    fuel_level: Optional[Decimal] = None

    odometer_reading: Optional[int] = None

    damage_notes: Optional[str] = None

    photo_urls: Optional[List[str]] = None

    video_url: Optional[str] = None


class RentalInspectionCreate(RentalInspectionBase):

    rental_id: UUID


class RentalInspectionResponse(RentalInspectionBase):

    id: UUID

    rental_id: UUID

    inspector_user_id: UUID

    inspected_at: datetime

    class Config:
        from_attributes = True



class RentedVehicleDamageReportBase(BaseModel):

    damage_type: str

    description: Optional[str] = None

    estimated_repair_cost: Optional[float] = None


class RentedVehicleDamageReportCreate(RentedVehicleDamageReportBase):

    vehicle_id: UUID


class RentedVehicleDamageReportResponse(RentedVehicleDamageReportBase):

    id: UUID

    vehicle_id: UUID

    reported_by: UUID

    damage_photo: Optional[str]

    status: str

    created_at: datetime

    class Config:
        from_attributes = True



class RentedVehicleAvailabilityBase(BaseModel):

    available_from: datetime

    available_to: datetime


class RentedVehicleAvailabilityCreate(RentedVehicleAvailabilityBase):

    vehicle_id: UUID


class RentedVehicleAvailabilityResponse(RentedVehicleAvailabilityBase):

    id: UUID

    vehicle_id: UUID

    is_booked: bool

    created_at: datetime

    class Config:
        from_attributes = True




