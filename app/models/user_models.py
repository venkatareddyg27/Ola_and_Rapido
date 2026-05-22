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
 
 
class User(Base):
    __tablename__ = "users"
 
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
 
    mobile_number = Column(String(20), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True)
 
    first_name = Column(String(60))
    last_name = Column(String(60))
    full_name = Column(String(100))
 
    profile_photo_url = Column(String(255))
 
    role = Column(Enum(UserRole), default=UserRole.CUSTOMER)
    status = Column(Enum(UserStatus), default=UserStatus.PENDING)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
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

    owned_vehicles = relationship(
        "Vehicle",
        back_populates="owner",
        cascade="all, delete-orphan"
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

    customer_trips = relationship(
        "Trip",
        back_populates="customer"
    )

    payments = relationship(
        "Payment",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    wallet = relationship(
        "Wallet",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    rentals_as_renter = relationship(
    "Rental",
    foreign_keys="Rental.renter_id",
    back_populates="renter",
    cascade="all, delete-orphan"
    )

    rentals_as_owner = relationship(
        "Rental",
        foreign_keys="Rental.owner_id",
        back_populates="owner",
        cascade="all, delete-orphan"
    )

    rental_inspections = relationship(
        "RentalInspection",
        foreign_keys="RentalInspection.inspector_user_id",
        back_populates="inspector",
        cascade="all, delete-orphan"
    )
    
    ratings_given = relationship(
    "Rating",
    foreign_keys="Rating.rater_id",
    back_populates="rater",
    cascade="all, delete-orphan"
    )

    ratings_received = relationship(
        "Rating",
        foreign_keys="Rating.ratee_id",
        back_populates="ratee",
        cascade="all, delete-orphan"
    )

    notifications = relationship(
        "Notification",
        back_populates="user",
        cascade="all, delete-orphan"
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
    promo_codes = relationship(
    "PromoCode",
    back_populates="user",
    cascade="all, delete-orphan")
    
    promo_codes = relationship(
    "PromoCode",
    foreign_keys="PromoCode.created_by",
    back_populates="creator",
    cascade="all, delete-orphan"
    )

    surge_zones = relationship(
        "SurgeZone",
        foreign_keys="SurgeZone.created_by",
        back_populates="creator",
        cascade="all, delete-orphan"
    )

    audit_logs = relationship(
        "AuditLog",
        foreign_keys="AuditLog.actor_id",
        back_populates="actor",
        cascade="all, delete-orphan"
    )
    
    
    

class DriverProfile(Base):

    __tablename__ = "driver_profiles"

    # =====================================================
    # PRIMARY KEY
    # =====================================================

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    # =====================================================
    # FOREIGN KEYS
    # =====================================================

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    vehicle_id = Column(
        UUID(as_uuid=True),
        ForeignKey("vehicles.id"),
        nullable=True
    )

    # =====================================================
    # DRIVER DETAILS
    # =====================================================

    subscription_plan = Column(
        Enum(SubscriptionPlan),
        default=SubscriptionPlan.BASIC
    )

    commission_rate = Column(
        Numeric(5, 2),
        default=10.00
    )

    # =====================================================
    # BANK DETAILS
    # =====================================================

    bank_account_number = Column(
        String(100),
        nullable=True
    )

    ifsc_code = Column(
        String(50),
        nullable=True
    )

    upi_id = Column(
        String(100),
        nullable=True
    )

    # =====================================================
    # PROFILE
    # =====================================================

    selfie_url = Column(
        String(255),
        nullable=True
    )

    # =====================================================
    # DRIVER STATUS
    # =====================================================

    status = Column(
        Enum(DriverStatus),
        default=DriverStatus.OFFLINE
    )

    is_verified = Column(
        Boolean,
        default=False
    )

    rating = Column(
        Numeric(3, 2),
        default=5.0
    )

    total_trips = Column(
        Integer,
        default=0
    )

    # =====================================================
    # TIMESTAMPS
    # =====================================================

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
        cascade="all, delete-orphan"
    )

    locations = relationship(
        "DriverLocation",
        back_populates="driver",
        cascade="all, delete-orphan"
    )
 
 ## kyc documents
 
class KYCDocument(Base):
    __tablename__ = "kyc_documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    # LICENSE DOCUMENTS
    license_number = Column(String(100), nullable=True)
    license_front_url = Column(String(255), nullable=True)
    license_back_url = Column(String(255), nullable=True)

    # AADHAAR DOCUMENTS
    aadhaar_number = Column(String(20), nullable=True)
    aadhaar_front_url = Column(String(255), nullable=True)
    aadhaar_back_url = Column(String(255), nullable=True)

    # PAN DOCUMENTS
    pan_number = Column(String(20), nullable=True)
    pan_front_url = Column(String(255), nullable=True)

    # VEHICLE DOCUMENTS
    rc_number = Column(String(100), nullable=True)
    rc_front_url = Column(String(255), nullable=True)
    rc_back_url = Column(String(255), nullable=True)

    insurance_url = Column(String(255), nullable=True)
    pollution_certificate_url = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    verification_status = Column(String(50), default="pending")
    # RELATIONSHIP
    user = relationship(
        "User",
        back_populates="kyc_documents"
    )
 
 
 ## kyc otp logs
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
 
 
class DriverLocation(Base):
    __tablename__ = "driver_locations"
 
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
 
    # =====================================================
    # FOREIGN KEYS
    # =====================================================
 
    driver_id = Column(
        UUID(as_uuid=True),
        ForeignKey("driver_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
 
    # =====================================================
    # LOCATION DATA
    # =====================================================
 
    latitude = Column(
        Numeric(10, 7),
        nullable=False
    )
 
    longitude = Column(
        Numeric(10, 7),
        nullable=False
    )
 
    heading = Column(
        Numeric(6, 2),
        nullable=True
    )
 
    speed = Column(
        Numeric(6, 2),
        nullable=True
    )
 
    is_active = Column(
        Boolean,
        default=True
    )
 
    # =====================================================
    # TIMESTAMPS
    # =====================================================
 
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
        back_populates="locations"
    )
