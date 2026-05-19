# users.py

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

from models.base import Base
from core.enums import (
    UserRole,
    UserStatus,
    DriverStatus,
    SubscriptionPlan, 
    OTPPurpose,
)


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
    status = Column(Enum(UserStatus), default=UserStatus.PENDING)

    created_at = Column(DateTime, default=datetime.utcnow)
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

    wallet = relationship(
        "Wallet",
        back_populates="user",
        uselist=False
    )

    kyc_documents = relationship(
        "KYCDocument",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    owned_vehicles = relationship(
        "Vehicle",
        back_populates="owner"
    )

    customer_trips = relationship(
        "Trip",
        foreign_keys="Trip.customer_id",
        back_populates="customer"
    )

    rentals_as_renter = relationship(
        "Rental",
        foreign_keys="Rental.renter_id",
        back_populates="renter"
    )

    rentals_as_owner = relationship(
        "Rental",
        foreign_keys="Rental.owner_id",
        back_populates="owner"
    )

    payments = relationship(
        "Payment",
        back_populates="user"
    )

    notifications = relationship(
        "Notification",
        back_populates="user"
    )

    ratings_given = relationship(
        "Rating",
        foreign_keys="Rating.rater_id",
        back_populates="rater"
    )

    ratings_received = relationship(
        "Rating",
        foreign_keys="Rating.ratee_id",
        back_populates="ratee"
    )

    disputes = relationship(
        "Dispute",
        foreign_keys="Dispute.user_id",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    resolved_disputes = relationship(
        "Dispute",
        foreign_keys="Dispute.resolved_by",
        back_populates="resolver"
    )
    otp_logs = relationship(
        "OTPLog",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    promo_codes = relationship(
    "PromoCode",
    back_populates="creator"
    )

    surge_zones = relationship(
        "SurgeZone",
        back_populates="creator"
    )

    audit_logs = relationship(
        "AuditLog",
        back_populates="actor"
    )
    
    
    
    
class DriverProfile(Base):
    __tablename__ = "driver_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        unique=True
    )

    vehicle_id = Column(
        UUID(as_uuid=True),
        ForeignKey("vehicles.id")
    )

    subscription_plan = Column(
        Enum(SubscriptionPlan),
        default=SubscriptionPlan.BASIC
    )

    commission_rate = Column(Numeric(5, 2))

    status = Column(
        Enum(DriverStatus),
        default=DriverStatus.OFFLINE
    )

    rating = Column(Numeric(3, 2), default=5.0)

    total_trips = Column(Integer, default=0)

    # RELATIONSHIPS

    user = relationship(
        "User",
        back_populates="driver_profile"
    )

    vehicle = relationship(
        "Vehicle",
        back_populates="drivers"
    )

    trips = relationship(
        "Trip",
        back_populates="driver"
    )

    subscriptions = relationship(
        "DriverSubscription",
        back_populates="driver",
        cascade="all, delete-orphan"
    )
    
    payouts = relationship(
    "DriverPayout",
    back_populates="driver",
    cascade="all, delete-orphan")


class KYCDocument(Base):
    __tablename__ = "kyc_documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id")
    )

    doc_url = Column(String(255), nullable=False)

    # RELATIONSHIPS

    user = relationship(
        "User",
        back_populates="kyc_documents"
    )

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

    # =====================================================
    # RELATIONSHIPS
    # =====================================================

    user = relationship(
        "User",
        back_populates="otp_logs"
    )
    
    
    

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

    # =====================================================
    # RELATIONSHIPS
    # =====================================================

    driver = relationship(
        "DriverProfile",
        back_populates="subscriptions"
    )
