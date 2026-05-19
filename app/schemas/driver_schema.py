from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

from core.enums import (
    AttendanceStatus,
    DriverDocumentType,
    DriverStatus,
    OnlineStatus,
    PayoutMethod,
    PayoutStatus,
    PenaltyStatus,
    ShiftStatus,
    VerificationStatus,
)


# =========================================================
# DRIVER PROFILE
# =========================================================

class DriverProfileBase(BaseModel):
    user_id: int
    license_number: str
    license_expiry: date
    current_vehicle_id: Optional[int] = None


class DriverProfileCreate(DriverProfileBase):
    pass


class DriverProfileResponse(DriverProfileBase):
    id: int
    driver_rating: Decimal
    total_rides: int
    online_status: OnlineStatus
    status: DriverStatus
    created_at: datetime

    class Config:
        from_attributes = True


# =========================================================
# DRIVER DOCUMENT
# =========================================================

class DriverDocumentCreate(BaseModel):
    driver_id: int
    document_type: DriverDocumentType
    document_url: str


class DriverDocumentResponse(BaseModel):
    id: int
    driver_id: int
    document_type: DriverDocumentType
    document_url: str
    verification_status: VerificationStatus
    uploaded_at: datetime

    class Config:
        from_attributes = True
      