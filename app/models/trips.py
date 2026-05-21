

import uuid

from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    DateTime,
    Enum,
    ForeignKey,
    Numeric,
    Boolean
)

from sqlalchemy.dialects.postgresql import (
    UUID
)

from sqlalchemy.orm import (
    relationship
)

from app.core.database import Base

from app.core.enums import (
    ServiceType,
    TripStatus,
    VehicleCategory
)

# =========================================================
# TRIP MODEL
# =========================================================

class Trip(Base):

    __tablename__ = "trips"

    # =====================================================
    # PRIMARY KEY
    # =====================================================

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    # =====================================================
    # USER RELATIONS
    # =====================================================

    customer_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    driver_id = Column(
        UUID(as_uuid=True),
        ForeignKey("driver_profiles.id"),
        nullable=True
    )

    # =====================================================
    # ADDRESS DETAILS
    # =====================================================

    pickup_address = Column(
        String(255),
        nullable=False
    )

    drop_address = Column(
        String(255),
        nullable=False
    )

    # =====================================================
    # LOCATION COORDINATES
    # =====================================================

    pickup_lat = Column(
        Numeric(10, 7),
        nullable=False
    )

    pickup_lng = Column(
        Numeric(10, 7),
        nullable=False
    )

    drop_lat = Column(
        Numeric(10, 7),
        nullable=False
    )

    drop_lng = Column(
        Numeric(10, 7),
        nullable=False
    )

    # =====================================================
    # SERVICE DETAILS
    # =====================================================

    service_type = Column(
        Enum(ServiceType),
        nullable=False
    )

    vehicle_category = Column(
        Enum(VehicleCategory),
        nullable=True
    )

    status = Column(
        Enum(TripStatus),
        default=TripStatus.SEARCHING_DRIVER,
        nullable=False
    )

    # =====================================================
    # FARE DETAILS
    # =====================================================

    fare = Column(
        Numeric(10, 2),
        nullable=True
    )

    estimated_fare = Column(
        Numeric(10, 2),
        nullable=True
    )

    estimated_distance = Column(
        Numeric(10, 2),
        nullable=True
    )

    surge_multiplier = Column(
        Numeric(4, 2),
        default=1.0
    )

    waiting_charge = Column(
        Numeric(10, 2),
        default=0
    )

    toll_charge = Column(
        Numeric(10, 2),
        default=0
    )

    # =====================================================
    # OTP
    # =====================================================

    ride_otp = Column(
        String(6),
        nullable=True
    )

    # =====================================================
    # SCHEDULE
    # =====================================================

    scheduled_time = Column(
        DateTime,
        nullable=True
    )

    # =====================================================
    # TIMESTAMPS
    # =====================================================

    started_at = Column(
        DateTime,
        nullable=True
    )

    completed_at = Column(
        DateTime,
        nullable=True
    )

    cancelled_at = Column(
        DateTime,
        nullable=True
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
    # CANCELLATION
    # =====================================================

    cancel_reason = Column(
        String(255),
        nullable=True
    )

    # =====================================================
    # FLAGS
    # =====================================================

    payment_completed = Column(
        Boolean,
        default=False
    )

    is_customer_rated = Column(
        Boolean,
        default=False
    )

    is_driver_rated = Column(
        Boolean,
        default=False
    )

    # =====================================================
    # RELATIONSHIPS
    # =====================================================

    customer = relationship(
        "User",
        back_populates="customer_trips"
    )

    driver = relationship(
        "DriverProfile",
        back_populates="trips"
    )

    parcel = relationship(
        "TripParcel",
        back_populates="trip",
        uselist=False,
        cascade="all, delete-orphan"
    )

    locations = relationship(
        "TripLocation",
        back_populates="trip",
        cascade="all, delete-orphan"
    )

    payments = relationship(
        "Payment",
        back_populates="trip",
        cascade="all, delete-orphan"
    )

    ratings = relationship(
        "Rating",
        back_populates="trip",
        cascade="all, delete-orphan"
    )

    disputes = relationship(
        "Dispute",
        back_populates="trip",
        cascade="all, delete-orphan"
    )

# =========================================================
# TRIP LOCATION MODEL
# =========================================================

class TripLocation(Base):

    __tablename__ = "trip_locations"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    trip_id = Column(
        UUID(as_uuid=True),
        ForeignKey("trips.id"),
        nullable=False
    )

    lat = Column(
        Numeric(10, 7),
        nullable=False
    )

    lng = Column(
        Numeric(10, 7),
        nullable=False
    )

    recorded_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    # =====================================================
    # RELATIONSHIP
    # =====================================================

    trip = relationship(
        "Trip",
        back_populates="locations"
    )

# =========================================================
# PARCEL MODEL
# =========================================================

class TripParcel(Base):

    __tablename__ = "parcels"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    trip_id = Column(
        UUID(as_uuid=True),
        ForeignKey("trips.id"),
        unique=True,
        nullable=False
    )

    sender_name = Column(
        String(100),
        nullable=False
    )

    sender_phone = Column(
        String(20),
        nullable=False
    )

    receiver_name = Column(
        String(100),
        nullable=False
    )

    receiver_phone = Column(
        String(20),
        nullable=False
    )

    receiver_address = Column(
        String(255),
        nullable=False
    )

    package_type = Column(
        String(50)
    )

    weight_kg = Column(
        Numeric(5, 2)
    )

    cod_amount = Column(
        Numeric(10, 2),
        default=0.0
    )

    pod_photo_url = Column(
        String(255)
    )

    pod_signature_url = Column(
        String(255)
    )

    pod_otp = Column(
        String(6)
    )

    status = Column(
        String(50),
        default="pending"
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
    # RELATIONSHIP
    # =====================================================

    trip = relationship(
        "Trip",
        back_populates="parcel"
    )