from datetime import date, time, datetime
from decimal import Decimal
from typing import Optional, List, Dict, Any
 
from pydantic import BaseModel, ConfigDict
 
from app.core.enums import (
    RentalBookingStatus,
    DamageClaimStatus,
    RentalExtensionStatus,
    ChecklistType,
    InspectionType,
)
 
# =========================================================
# RENTAL BOOKING SCHEMA
# =========================================================
 
class RentalBookingCreate(BaseModel):
    customer_id: int
    owner_id: int
    vehicle_id: int
 
    pickup_date: date
    return_date: date
    pickup_time: Optional[time] = None
    return_time: Optional[time] = None
 
    total_days: int
 
    pickup_location: Optional[str] = None
    return_location: Optional[str] = None
 
    daily_rate: Decimal
    total_rental_amount: Decimal
    security_deposit_amount: Decimal
 
    km_limit_included: Optional[int] = None
    per_km_overage_rate: Optional[Decimal] = None
 
 
class RentalBookingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
 
    id: int
 
    customer_id: int
    owner_id: int
    vehicle_id: int
 
    pickup_date: date
    return_date: date
    pickup_time: Optional[time]
    return_time: Optional[time]
 
    total_days: int
 
    pickup_location: Optional[str]
    return_location: Optional[str]
 
    daily_rate: Decimal
    total_rental_amount: Decimal
    security_deposit_amount: Decimal
 
    km_limit_included: Optional[int]
    per_km_overage_rate: Optional[Decimal]
 
    renter_kyc_verified_at: Optional[datetime]
 
    status: RentalBookingStatus
 
    created_at: datetime
    updated_at: datetime
 
 
# =========================================================
# RENTAL EXTENSION SCHEMA
# =========================================================
 
class RentalExtensionCreate(BaseModel):
    booking_id: int
    old_end_date: date
    new_end_date: date
    extra_amount: Decimal
 
 
class RentalExtensionResponse(RentalExtensionCreate):
    id: int
    status: RentalExtensionStatus
    created_at: datetime
 
    model_config = ConfigDict(from_attributes=True)
 
 
# =========================================================
# TRIP LOG SCHEMA
# =========================================================
 
class RentalTripLogCreate(BaseModel):
    booking_id: int
    start_km: int
    end_km: Optional[int] = None
 
    fuel_before: Optional[Decimal] = None
    fuel_after: Optional[Decimal] = None
 
    extra_km_charge: Optional[Decimal] = 0
 
 
class RentalTripLogResponse(RentalTripLogCreate):
    id: int
    created_at: datetime
 
    model_config = ConfigDict(from_attributes=True)
 
 
# =========================================================
# SECURITY DEPOSIT SCHEMA
# =========================================================
 
class RentalSecurityDepositCreate(BaseModel):
    booking_id: int
    deposit_amount: Decimal
 
 
class RentalSecurityDepositResponse(RentalSecurityDepositCreate):
    id: int
 
    refund_amount: Decimal
    deduction_amount: Decimal
    refund_status: str
    refund_date: Optional[datetime]
 
    created_at: datetime
 
    model_config = ConfigDict(from_attributes=True)
 
 
# =========================================================
# CHECKLIST SCHEMA
# =========================================================
 
class RentalChecklistCreate(BaseModel):
    booking_id: int
    checklist_type: ChecklistType
 
    helmet_available: bool = False
    rc_available: bool = False
    insurance_available: bool = False
 
    vehicle_condition: Optional[str] = None
    customer_signature: Optional[str] = None
 
 
class RentalChecklistResponse(RentalChecklistCreate):
    id: int
    created_at: datetime
 
    model_config = ConfigDict(from_attributes=True)
 
 
# =========================================================
# FUEL LOG SCHEMA
# =========================================================
 
class RentalFuelLogCreate(BaseModel):
    booking_id: int
    fuel_level: Decimal
 
    fuel_cost: Optional[Decimal] = None
    fuel_station: Optional[str] = None
    receipt_image: Optional[str] = None
 
 
class RentalFuelLogResponse(RentalFuelLogCreate):
    id: int
    created_at: datetime
 
    model_config = ConfigDict(from_attributes=True)
 
 
# =========================================================
# DAMAGE REPORT SCHEMA
# =========================================================
 
class RentalDamageReportCreate(BaseModel):
    booking_id: int
    damage_description: str
 
    damage_cost: Optional[Decimal] = 0
    proof_images: Optional[List[Dict[str, Any]]] = None
 
 
class RentalDamageReportResponse(RentalDamageReportCreate):
    id: int
    report_status: DamageClaimStatus
    created_at: datetime
 
    model_config = ConfigDict(from_attributes=True)
 
 
# =========================================================
# INSPECTION SCHEMA
# =========================================================
 
class RentalInspectionCreate(BaseModel):
    booking_id: int
    inspection_type: InspectionType
 
    inspected_by: Optional[int] = None
 
    odometer: Optional[int] = None
    fuel_level: Optional[str] = None
 
    notes: Optional[str] = None
    images: Optional[List[Dict[str, Any]]] = None
    video_url: Optional[str] = None
 
    completed_at: Optional[datetime] = None
 
 
class RentalInspectionResponse(RentalInspectionCreate):
    id: int
    created_at: datetime
 
    model_config = ConfigDict(from_attributes=True)
 