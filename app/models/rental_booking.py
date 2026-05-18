from datetime import datetime

from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    String,
    Text,
    Date,
    Time,
    DateTime,
    Boolean,
    Numeric,
    ForeignKey,
    Enum as SqlEnum,
)
from sqlalchemy.dialects.postgresql import JSONB

from app.core.database import Base
from app.core.enums import RentalBookingStatus, DamageClaimStatus


class RentalBooking(Base):
    __tablename__ = "rental_bookings"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)

    customer_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    owner_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    listing_id = Column(BigInteger, ForeignKey("listings.id", ondelete="CASCADE"), nullable=False, index=True)
    vehicle_id = Column(BigInteger, ForeignKey("vehicles.id", ondelete="CASCADE"), nullable=False, index=True)

    pickup_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=False)
    pickup_time = Column(Time, nullable=True)
    return_time = Column(Time, nullable=True)

    total_days = Column(Integer, nullable=False)

    pickup_location = Column(Text, nullable=True)
    return_location = Column(Text, nullable=True)

    daily_rate = Column(Numeric(10, 2), nullable=False)
    total_rental_amount = Column(Numeric(10, 2), nullable=False)
    security_deposit_amount = Column(Numeric(10, 2), nullable=False)

    km_limit_included = Column(Integer, nullable=True)
    per_km_overage_rate = Column(Numeric(10, 2), nullable=True)

    renter_kyc_verified_at = Column(DateTime, nullable=True)

    rental_agreement_signed_url = Column(Text, nullable=True)
    rental_agreement_signed_at = Column(DateTime, nullable=True)

    pre_inspection_photos = Column(JSONB, default=list, nullable=False)
    pre_inspection_video_url = Column(Text, nullable=True)
    pre_inspection_odometer = Column(Integer, nullable=True)
    pre_inspection_fuel_level = Column(String(20), nullable=True)
    pre_inspection_notes = Column(Text, nullable=True)
    pre_inspection_completed_at = Column(DateTime, nullable=True)

    post_inspection_photos = Column(JSONB, default=list, nullable=False)
    post_inspection_video_url = Column(Text, nullable=True)
    post_inspection_odometer = Column(Integer, nullable=True)
    post_inspection_fuel_level = Column(String(20), nullable=True)
    actual_km_driven = Column(Integer, nullable=True)
    fuel_shortage_liters = Column(Numeric(10, 2), nullable=True)
    fuel_recharge_amount = Column(Numeric(10, 2), nullable=True)
    post_inspection_completed_at = Column(DateTime, nullable=True)

    damage_reported = Column(Boolean, default=False, nullable=False)
    damage_amount = Column(Numeric(10, 2), nullable=True)
    damage_photos = Column(JSONB, default=list, nullable=False)

    damage_claim_status = Column(
        SqlEnum(DamageClaimStatus),
        default=DamageClaimStatus.NONE,
        nullable=False,
    )

    status = Column(
        SqlEnum(RentalBookingStatus),
        default=RentalBookingStatus.PENDING,
        nullable=False,
    )

    escrow_payment_id = Column(BigInteger, ForeignKey("payments.id", ondelete="SET NULL"), nullable=True)

    escrow_released_at = Column(DateTime, nullable=True)

    security_deposit_held = Column(Boolean, default=True, nullable=False)
    security_deposit_released_at = Column(DateTime, nullable=True)

    final_total_amount = Column(Numeric(10, 2), nullable=True)
    refund_amount = Column(Numeric(10, 2), nullable=True)

    customer_rating = Column(Numeric(2, 1), nullable=True)
    owner_rating = Column(Numeric(2, 1), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )