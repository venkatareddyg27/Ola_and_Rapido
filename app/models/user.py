from datetime import datetime

from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Boolean,
    Text,
    Date,
    DateTime,
    Integer,
    Numeric,
    ForeignKey,
    Enum as SqlEnum,
)

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.core.database import Base

from app.core.enums import (
    Gender,
    UserRole,
    KYCStatus,
    LoyaltyTier,
    DriverStatus,
)


# =========================================================
# USER MODEL
# =========================================================

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)

    phone_number = Column(
        String(15),
        unique=True,
        nullable=False,
        index=True,
    )

    email = Column(
        String(255),
        unique=True,
        nullable=True,
        index=True,
    )

    full_name = Column(String(255), nullable=False)

    role = Column(SqlEnum(UserRole), nullable=False)

    hashed_password = Column(String(255), nullable=True)

    firebase_uid = Column(
        String(255),
        unique=True,
        nullable=True,
        index=True,
    )

    is_phone_verified = Column(Boolean, default=False, nullable=False)

    is_active = Column(Boolean, default=True, nullable=False)

    is_blocked = Column(Boolean, default=False, nullable=False)

    blocked_reason = Column(Text, nullable=True)

    profile_photo_url = Column(Text, nullable=True)

    date_of_birth = Column(Date, nullable=True)

    gender = Column(SqlEnum(Gender), nullable=True)

    emergency_contacts = Column(JSONB, default=list, nullable=False)

    preferred_language = Column(String(10), default="en", nullable=False)

    notification_settings = Column(JSONB, default=dict, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    last_login_at = Column(DateTime, nullable=True)

    # Relationships
    customer_profile = relationship(
        "CustomerProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete",
    )

    driver_profile = relationship(
        "DriverProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete",
    )

    car_owner_profile = relationship(
        "CarOwnerProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete",
    )


# =========================================================
# CUSTOMER PROFILE MODEL
# =========================================================

class CustomerProfile(Base):
    __tablename__ = "customer_profiles"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)

    user_id = Column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    kyc_status = Column(
        SqlEnum(KYCStatus),
        default=KYCStatus.NOT_STARTED,
        nullable=False,
    )

    kyc_rejection_reason = Column(Text, nullable=True)

    kyc_approved_at = Column(DateTime, nullable=True)

    kyc_expires_at = Column(DateTime, nullable=True)

    saved_addresses = Column(JSONB, default=list, nullable=False)

    total_rides = Column(Integer, default=0, nullable=False)

    total_parcels = Column(Integer, default=0, nullable=False)

    total_rentals = Column(Integer, default=0, nullable=False)

    lifetime_spent = Column(Numeric(12, 2), default=0, nullable=False)

    average_rating = Column(Numeric(3, 2), default=5.0, nullable=False)

    loyalty_points = Column(Integer, default=0, nullable=False)

    loyalty_tier = Column(
        SqlEnum(LoyaltyTier),
        default=LoyaltyTier.BRONZE,
        nullable=False,
    )

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    # Relationships
    user = relationship(
    "User",
    back_populates="customer_profile",)
    

# =========================================================
# DRIVER PROFILE MODEL
# =========================================================

class DriverProfile(Base):
    __tablename__ = "driver_profiles"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)

    user_id = Column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    current_vehicle_id = Column(
        BigInteger,
        ForeignKey("vehicles.id", ondelete="SET NULL"))

    is_online = Column(Boolean, default=False, nullable=False)

    current_status = Column(
        SqlEnum(DriverStatus),
        default=DriverStatus.IDLE,
        nullable=False,
    )

    break_mode_until = Column(DateTime, nullable=True)

    current_city = Column(String(100), nullable=True)

    current_zone = Column(String(100), nullable=True)

    total_earnings = Column(Numeric(12, 2), default=0, nullable=False)

    total_rides_completed = Column(Integer, default=0, nullable=False)

    total_parcels_delivered = Column(Integer, default=0, nullable=False)

    cancellation_rate = Column(Numeric(5, 2), default=0, nullable=False)

    acceptance_rate = Column(Numeric(5, 2), default=0, nullable=False)

    average_rating = Column(Numeric(3, 2), default=5.0, nullable=False)

    wallet_balance = Column(Numeric(12, 2), default=0, nullable=False)

    bank_account_name = Column(String(255), nullable=True)

    bank_account_number = Column(String(50), nullable=True)

    bank_ifsc = Column(String(20), nullable=True)

    upi_id = Column(String(100), nullable=True)

    dl_verified = Column(Boolean, default=False, nullable=False)

    rc_verified = Column(Boolean, default=False, nullable=False)

    puc_verified = Column(Boolean, default=False, nullable=False)

    insurance_verified = Column(Boolean, default=False, nullable=False)

    background_check_completed = Column(Boolean, default=False, nullable=False)

    last_latitude = Column(Numeric(10, 8), nullable=True)

    last_longitude = Column(Numeric(11, 8), nullable=True)

    last_location_update = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    user = relationship(
    "User",
    back_populates="driver_profile")

# =========================================================
# CAR OWNER PROFILE MODEL
# =========================================================

class CarOwnerProfile(Base):
    __tablename__ = "car_owner_profiles"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)

    user_id = Column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    kyc_status = Column(
        SqlEnum(KYCStatus),
        default=KYCStatus.NOT_STARTED,
        nullable=False,
    )

    pan_verified = Column(Boolean, default=False, nullable=False)

    pan_number = Column(String(10), nullable=True)

    aadhaar_verified = Column(Boolean, default=False, nullable=False)

    aadhaar_tokenized_id = Column(String(100), nullable=True)

    bank_account_verified = Column(Boolean, default=False, nullable=False)

    bank_account_name = Column(String(255), nullable=True)

    bank_account_number = Column(String(50), nullable=True)

    bank_ifsc = Column(String(20), nullable=True)

    upi_id = Column(String(100), nullable=True)

    total_listings = Column(Integer, default=0, nullable=False)

    total_rentals_completed = Column(Integer, default=0, nullable=False)

    total_earnings = Column(Numeric(12, 2), default=0, nullable=False)

    average_rating = Column(Numeric(3, 2), default=5.0, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    user = relationship(
    "User",
    back_populates="car_owner_profile")