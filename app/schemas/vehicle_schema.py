from datetime import datetime
from decimal import Decimal
from typing import Optional, List

from pydantic import BaseModel

from app.models.vehicle import (
    VehicleType,
    FuelType,
    TransmissionType,
    VehicleVerificationStatus
)


# =========================================================
# VEHICLE CREATE
# =========================================================

class VehicleCreateSchema(BaseModel):

    owner_id: int

    vehicle_type: VehicleType

    brand: str

    model: str

    year: int

    registration_number: str

    color: Optional[str] = None

    fuel_type: FuelType

    transmission_type: TransmissionType

    seating_capacity: Optional[int] = None

    description: Optional[str] = None

    price_per_day: Decimal


# =========================================================
# VEHICLE UPDATE
# =========================================================

class VehicleUpdateSchema(BaseModel):

    color: Optional[str] = None

    description: Optional[str] = None

    price_per_day: Optional[Decimal] = None

    is_available: Optional[bool] = None

    verification_status: Optional[
        VehicleVerificationStatus
    ] = None


# =========================================================
# VEHICLE RESPONSE
# =========================================================

class VehicleResponseSchema(BaseModel):

    id: int

    owner_id: int

    vehicle_type: VehicleType

    brand: str

    model: str

    year: int

    registration_number: str

    color: Optional[str]

    fuel_type: FuelType

    transmission_type: TransmissionType

    seating_capacity: Optional[int]

    description: Optional[str]

    price_per_day: Decimal

    is_available: bool

    verification_status: VehicleVerificationStatus

    created_at: datetime

    updated_at: datetime

    class Config:
        from_attributes = True