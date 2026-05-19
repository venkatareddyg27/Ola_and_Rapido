
import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    DateTime,
    Enum,
    ForeignKey,
    Numeric,
    Integer,
    Boolean
)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base

from app.core.enums import (
    UserRole,
    UserStatus,
    DriverStatus,
    SubscriptionPlan,
    OTPPurpose,
)


# =====================================================
# USER MODEL
# =====================================================

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    phone = Column(String(20), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True)

    first_name = Column(String(60))
    last_name = Column(String(60))
    full_name = Column(String(100))

    profile_photo_url = Column(String(255))

    role = Column(Enum(UserRole), default=UserRole.CUSTOMER)

    status = Column(
        Enum(UserStatus),
        default=UserStatus.PENDING
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # RELATIONSHIPS

    driver_profile = relationship(
        "DriverProfile",
        back_populates="user",
        uselist=False
    )

    kyc_documents = relationship(
        "KYCDocument",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    otp_logs = relationship(
        "OTPLog",
        back_populates="user",
        cascade="all, delete-orphan"
    )


# =====================================================
# DRIVER PROFILE MODEL
# =====================================================

class DriverProfile(Base):
    __tablename__ = "driver_profiles"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        unique=True
    )

    subscription_plan = Column(
        Enum(SubscriptionPlan),
        default=SubscriptionPlan.BASIC
    )

    commission_rate = Column(
        Numeric(5, 2)
    )

    status = Column(
        Enum(DriverStatus),
        default=DriverStatus.OFFLINE
    )

    rating = Column(
        Numeric(3, 2),
        default=5.0
    )

    total_trips = Column(
        Integer,
        default=0
    )

    # RELATIONSHIPS

    user = relationship(
        "User",
        back_populates="driver_profile"
    )

    subscriptions = relationship(
        "DriverSubscription",
        back_populates="driver",
        cascade="all, delete-orphan"
    )


# =====================================================
# KYC DOCUMENT MODEL
# =====================================================

class KYCDocument(Base):
    __tablename__ = "kyc_documents"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id")
    )

    doc_url = Column(
        String(255),
        nullable=False
    )

    # RELATIONSHIPS

    user = relationship(
        "User",
        back_populates="kyc_documents"
    )


# =====================================================
# OTP LOG MODEL
# =====================================================

class OTPLog(Base):
    __tablename__ = "otp_logs"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True
    )

    phone = Column(
        String(20),
        nullable=False,
        index=True
    )

    otp_hash = Column(
        String(255),
        nullable=False
    )

    purpose = Column(
        Enum(OTPPurpose),
        nullable=False
    )

    expires_at = Column(
        DateTime,
        nullable=False
    )

    used_at = Column(
        DateTime,
        nullable=True
    )

    attempts = Column(
        Integer,
        default=0,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    # RELATIONSHIPS

    user = relationship(
        "User",
        back_populates="otp_logs"
    )


# =====================================================
# DRIVER SUBSCRIPTION MODEL
# =====================================================

class DriverSubscription(Base):
    __tablename__ = "driver_subscriptions"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    driver_id = Column(
        UUID(as_uuid=True),
        ForeignKey("driver_profiles.id"),
        nullable=False
    )

    plan = Column(
        Enum(SubscriptionPlan),
        nullable=False
    )

    commission_rate = Column(
        Numeric(5, 2)
    )

    start_date = Column(
        DateTime,
        nullable=False
    )

    end_date = Column(
        DateTime,
        nullable=True
    )

    auto_renew = Column(
        Boolean,
        default=True
    )

    status = Column(
        String(20),
        default="active"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # RELATIONSHIPS

    driver = relationship(
        "DriverProfile",
        back_populates="subscriptions"
    )