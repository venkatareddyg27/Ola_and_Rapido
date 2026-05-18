from enum import Enum
from decimal import Decimal
from datetime import date, time, datetime
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, ConfigDict
from core.enums import DamageClaimStatus, RentalBookingStatus

class RentalBookingCreate(BaseModel):
    customer_id: int
    owner_id: int
    listing_id: int
    vehicle_id: int

    pickup_date: date
    return_date: date
    pickup_time: Optional[time] = None
    return_time: Optional[time] = None

    total_days: int

    pickup_location: Optional[str] = None
    return_location: Optional[str] = None

    km_limit_included: Optional[int] = None
    per_km_overage_rate: Optional[Decimal] = None

    customer_rating: Optional[Decimal] = None
    owner_rating: Optional[Decimal] = None


class RentalBookingUpdate(BaseModel):
    rental_agreement_signed_url: Optional[str] = None
    rental_agreement_signed_at: Optional[datetime] = None

    pre_inspection_photos: Optional[List[Dict[str, Any]]] = None
    pre_inspection_video_url: Optional[str] = None
    pre_inspection_odometer: Optional[int] = None
    pre_inspection_fuel_level: Optional[str] = None
    pre_inspection_notes: Optional[str] = None
    pre_inspection_completed_at: Optional[datetime] = None

    post_inspection_photos: Optional[List[Dict[str, Any]]] = None
    post_inspection_video_url: Optional[str] = None
    post_inspection_odometer: Optional[int] = None
    post_inspection_fuel_level: Optional[str] = None
    actual_km_driven: Optional[int] = None

    fuel_shortage_liters: Optional[Decimal] = None
    fuel_recharge_amount: Optional[Decimal] = None
    post_inspection_completed_at: Optional[datetime] = None

    damage_reported: Optional[bool] = None
    damage_amount: Optional[Decimal] = None
    damage_photos: Optional[List[Dict[str, Any]]] = None
    damage_claim_status: Optional[DamageClaimStatus] = None

    status: Optional[RentalBookingStatus] = None

    escrow_payment_id: Optional[int] = None
    escrow_released_at: Optional[datetime] = None

    security_deposit_held: Optional[bool] = None
    security_deposit_released_at: Optional[datetime] = None

    final_total_amount: Optional[Decimal] = None
    refund_amount: Optional[Decimal] = None

    customer_rating: Optional[Decimal] = None
    owner_rating: Optional[Decimal] = None


class RentalBookingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int

    customer_id: int
    owner_id: int
    listing_id: int
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

    rental_agreement_signed_url: Optional[str]
    rental_agreement_signed_at: Optional[datetime]

    pre_inspection_photos: List[Dict[str, Any]]
    pre_inspection_video_url: Optional[str]
    pre_inspection_odometer: Optional[int]
    pre_inspection_fuel_level: Optional[str]
    pre_inspection_notes: Optional[str]
    pre_inspection_completed_at: Optional[datetime]

    post_inspection_photos: List[Dict[str, Any]]
    post_inspection_video_url: Optional[str]
    post_inspection_odometer: Optional[int]
    post_inspection_fuel_level: Optional[str]
    actual_km_driven: Optional[int]

    fuel_shortage_liters: Optional[Decimal]
    fuel_recharge_amount: Optional[Decimal]
    post_inspection_completed_at: Optional[datetime]

    damage_reported: bool
    damage_amount: Optional[Decimal]
    damage_photos: List[Dict[str, Any]]
    damage_claim_status: DamageClaimStatus

    status: RentalBookingStatus

    escrow_payment_id: Optional[int]
    escrow_released_at: Optional[datetime]

    security_deposit_held: bool
    security_deposit_released_at: Optional[datetime]

    final_total_amount: Optional[Decimal]
    refund_amount: Optional[Decimal]

    customer_rating: Optional[Decimal]
    owner_rating: Optional[Decimal]

    created_at: datetime
    updated_at: datetime