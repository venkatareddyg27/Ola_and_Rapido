from datetime import datetime, date
from decimal import Decimal
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict

from app.core.enums import (
    FuelType,
    TransmissionType,
    VehicleVerificationStatus,
)


# =========================================================
# VEHICLE SCHEMAS
# =========================================================

class VehicleBase(BaseModel):

    registration_number: Optional[str] = Field(None, max_length=20)

    rc_photo_url: Optional[str] = None
    rc_owner_name: Optional[str] = None

    make: Optional[str] = None
    model: Optional[str] = None

    year: Optional[int] = Field(None, ge=2000)

    color: Optional[str] = None

    fuel_type: Optional[FuelType] = None
    transmission: Optional[TransmissionType] = None

    seating_capacity: Optional[int] = 5

    insurance_policy_number: Optional[str] = None
    insurance_valid_until: Optional[date] = None
    insurance_photo_url: Optional[str] = None

    puc_certificate_number: Optional[str] = None
    puc_valid_until: Optional[date] = None
    puc_photo_url: Optional[str] = None

    gps_tracker_imei: Optional[str] = None
    gps_tracker_installed: Optional[bool] = False


class VehicleCreate(VehicleBase):

    owner_user_id: int

    registration_number: str
    rc_photo_url: str

    make: str
    model: str

    year: int


class VehicleUpdate(VehicleBase):

    rc_verified: Optional[bool] = None

    verification_status: Optional[
        VehicleVerificationStatus
    ] = None

    is_active: Optional[bool] = None


class VehicleResponse(VehicleBase):

    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_user_id: int

    registration_number: str

    rc_verified: bool

    rc_verification_date: Optional[
        datetime
    ] = None

    verification_status: VehicleVerificationStatus

    is_active: bool

    created_at: datetime
    updated_at: datetime