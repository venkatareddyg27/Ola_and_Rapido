import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, ConfigDict

from app.core.enums import InspectionType


# =========================================================
# RENTAL SCHEMAS
# =========================================================

class RentalBase(BaseModel):
    vehicle_id: uuid.UUID
    renter_id: uuid.UUID
    owner_id: uuid.UUID
    total_fare: Decimal


class RentalCreate(RentalBase):
    pass


class RentalUpdate(BaseModel):
    vehicle_id: Optional[uuid.UUID] = None
    renter_id: Optional[uuid.UUID] = None
    owner_id: Optional[uuid.UUID] = None
    total_fare: Optional[Decimal] = None


class RentalResponse(RentalBase):
    id: uuid.UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# =========================================================
# RENTAL INSPECTION SCHEMAS
# =========================================================

class RentalInspectionBase(BaseModel):
    rental_id: uuid.UUID
    inspection_type: InspectionType

    fuel_level: Optional[Decimal] = None
    odometer_reading: Optional[int] = None

    damage_notes: Optional[str] = None
    photo_urls: Optional[List[str]] = None
    video_url: Optional[str] = None

    inspector_user_id: uuid.UUID
    inspected_at: datetime


class RentalInspectionCreate(RentalInspectionBase):
    pass


class RentalInspectionUpdate(BaseModel):
    inspection_type: Optional[InspectionType] = None

    fuel_level: Optional[Decimal] = None
    odometer_reading: Optional[int] = None

    damage_notes: Optional[str] = None
    photo_urls: Optional[List[str]] = None
    video_url: Optional[str] = None

    inspector_user_id: Optional[uuid.UUID] = None
    inspected_at: Optional[datetime] = None


class RentalInspectionResponse(RentalInspectionBase):
    id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)