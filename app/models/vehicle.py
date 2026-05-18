from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime,
    Date,
    Integer,
    BigInteger,
    Text,
    ForeignKey,
    Numeric,
    Enum as SQLEnum,
)

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from core.database import Base

from app.core.enums import (
    FuelType,
    TransmissionType,
    VehicleVerificationStatus,
)


# =========================================================
# VEHICLE MODEL
# =========================================================

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(BigInteger, primary_key=True, index=True)

    owner_user_id = Column(
        BigInteger,
        ForeignKey("users.id"),
        nullable=False
    )

    registration_number = Column(
        String(20),
        unique=True,
        nullable=False,
        index=True
    )

    rc_verified = Column(Boolean, default=False)
    rc_verification_date = Column(DateTime, nullable=True)

    rc_photo_url = Column(Text, nullable=False)
    rc_owner_name = Column(String(255), nullable=True)

    make = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)

    year = Column(Integer, nullable=False)
    color = Column(String(50), nullable=True)

    fuel_type = Column(
        SQLEnum(FuelType),
        nullable=True
    )

    transmission = Column(
        SQLEnum(TransmissionType),
        nullable=True
    )

    seating_capacity = Column(Integer, default=5)

    insurance_policy_number = Column(String(100), nullable=True)
    insurance_valid_until = Column(Date, nullable=True)
    insurance_photo_url = Column(Text, nullable=True)

    puc_certificate_number = Column(String(100), nullable=True)
    puc_valid_until = Column(Date, nullable=True)
    puc_photo_url = Column(Text, nullable=True)

    verification_status = Column(
        SQLEnum(VehicleVerificationStatus),
        default=VehicleVerificationStatus.PENDING
    )

    is_active = Column(Boolean, default=True)

    gps_tracker_imei = Column(String(50), nullable=True)
    gps_tracker_installed = Column(Boolean, default=False)

    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )


# =========================================================
# VEHICLE LISTING MODEL
# =========================================================

class VehicleListing(Base):
    __tablename__ = "vehicle_listings"

    id = Column(BigInteger, primary_key=True, index=True)

    vehicle_id = Column(
        BigInteger,
        ForeignKey("vehicles.id"),
        nullable=False
    )

    owner_user_id = Column(
        BigInteger,
        ForeignKey("users.id"),
        nullable=False
    )

    daily_rate = Column(
        Numeric(10, 2),
        nullable=False
    )

    per_km_rate = Column(
        Numeric(5, 2),
        nullable=True
    )

    security_deposit_amount = Column(
        Numeric(10, 2),
        nullable=False
    )

    minimum_rental_days = Column(
        Integer,
        default=1
    )

    maximum_rental_days = Column(
        Integer,
        default=30
    )

    available_from = Column(Date, nullable=True)
    available_until = Column(Date, nullable=True)

    is_available = Column(Boolean, default=True)

    pickup_latitude = Column(
        Numeric(10, 8),
        nullable=False
    )

    pickup_longitude = Column(
        Numeric(11, 8),
        nullable=False
    )

    pickup_address = Column(Text, nullable=True)

    photos = Column(JSONB, default=list)
    interior_photos = Column(JSONB, default=list)

    description = Column(Text, nullable=True)

    amenities = Column(JSONB, default=list)

    km_limit_per_day = Column(Integer, nullable=True)

    allowed_states = Column(JSONB, default=list)

    total_bookings = Column(Integer, default=0)

    total_revenue = Column(
        Numeric(12, 2),
        default=0
    )

    average_rating = Column(
        Numeric(3, 2),
        default=5.0
    )

    admin_approved = Column(Boolean, default=False)

    admin_approval_at = Column(DateTime, nullable=True)

    admin_notes = Column(Text, nullable=True)

    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )