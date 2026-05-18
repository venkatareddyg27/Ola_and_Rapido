
from enum import Enum
from decimal import Decimal
from datetime import datetime
from typing import Optional
from core.enums import RideType, RideStatus, PaymentMethod, PaymentStatus
from pydantic import BaseModel, ConfigDict, Field



class RideCreate(BaseModel):
    customer_id: int

    ride_type: RideType

    pickup_latitude: Decimal
    pickup_longitude: Decimal
    pickup_address: str
    pickup_landmark: Optional[str] = None

    drop_latitude: Optional[Decimal] = None
    drop_longitude: Optional[Decimal] = None
    drop_address: Optional[str] = None

    is_scheduled: Optional[bool] = False
    scheduled_for: Optional[datetime] = None

    promo_code: Optional[str] = Field(None, max_length=50)

    payment_method: PaymentMethod


class RideUpdate(BaseModel):
    driver_id: Optional[int] = None

    drop_latitude: Optional[Decimal] = None
    drop_longitude: Optional[Decimal] = None
    drop_address: Optional[str] = None

    waiting_charges: Optional[Decimal] = None
    toll_charges: Optional[Decimal] = None
    discount_amount: Optional[Decimal] = None

    final_fare: Optional[Decimal] = None

    status: Optional[RideStatus] = None
    cancellation_reason: Optional[str] = None
    cancelled_by: Optional[int] = None

    otp_verified_at: Optional[datetime] = None

    actual_distance_km: Optional[Decimal] = None
    actual_duration_minutes: Optional[int] = None
    route_polyline: Optional[str] = None

    payment_status: Optional[PaymentStatus] = None
    payment_id: Optional[int] = None

    customer_rating: Optional[Decimal] = None
    customer_feedback: Optional[str] = None

    driver_rating: Optional[Decimal] = None
    driver_feedback: Optional[str] = None


class RideResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int

    customer_id: int
    driver_id: Optional[int]

    ride_type: RideType

    pickup_latitude: Decimal
    pickup_longitude: Decimal
    pickup_address: str
    pickup_landmark: Optional[str]

    drop_latitude: Optional[Decimal]
    drop_longitude: Optional[Decimal]
    drop_address: Optional[str]

    is_scheduled: bool
    scheduled_for: Optional[datetime]

    base_fare: Optional[Decimal]
    distance_fare: Optional[Decimal]
    time_fare: Optional[Decimal]

    surge_multiplier: Decimal
    surge_contribution: Decimal

    waiting_charges: Decimal
    toll_charges: Decimal
    discount_amount: Decimal

    promo_code: Optional[str]

    total_fare: Decimal
    final_fare: Optional[Decimal]

    status: RideStatus
    cancellation_reason: Optional[str]
    cancelled_by: Optional[int]

    pickup_otp: Optional[str]
    otp_verified_at: Optional[datetime]

    driver_assigned_at: Optional[datetime]
    driver_arrived_at: Optional[datetime]
    trip_started_at: Optional[datetime]
    trip_ended_at: Optional[datetime]

    scheduled_ride_processed_at: Optional[datetime]

    actual_distance_km: Optional[Decimal]
    actual_duration_minutes: Optional[int]
    route_polyline: Optional[str]

    payment_method: PaymentMethod
    payment_status: PaymentStatus
    payment_id: Optional[int]

    customer_rating: Optional[Decimal]
    customer_feedback: Optional[str]

    driver_rating: Optional[Decimal]
    driver_feedback: Optional[str]

    created_at: datetime
    updated_at: datetime