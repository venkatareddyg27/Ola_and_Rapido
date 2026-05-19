
import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    DateTime,
    Enum,
    ForeignKey,
    Numeric
)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models.base import Base
from core.enums import (
    ServiceType,
    TripStatus
)


class Trip(Base):
    __tablename__ = "trips"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    customer_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id")
    )

    driver_id = Column(
        UUID(as_uuid=True),
        ForeignKey("driver_profiles.id")
    )

    pickup_address = Column(String(255))
    drop_address = Column(String(255))

    pickup_lat = Column(Numeric(10, 7))
    pickup_lng = Column(Numeric(10, 7))

    drop_lat = Column(Numeric(10, 7))
    drop_lng = Column(Numeric(10, 7))

    service_type = Column(Enum(ServiceType))

    status = Column(
        Enum(TripStatus),
        default=TripStatus.SEARCHING
    )

    fare = Column(Numeric(10, 2))
    surge_multiplier = Column(Numeric(4, 2), default=1.0)
    otp = Column(String(6))
    scheduled_time = Column(DateTime)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    cancelled_at = Column(DateTime)
    cancellation_reason = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

    # RELATIONSHIPS

    customer = relationship(
        "User",
        foreign_keys=[customer_id],
        back_populates="customer_trips"
    )

    driver = relationship(
        "DriverProfile",
        back_populates="trips"
    )

    locations = relationship(
        "TripLocation",
        back_populates="trip",
        cascade="all, delete-orphan"
    )

    payments = relationship(
        "Payment",
        back_populates="trip"
    )

    ratings = relationship(
        "Rating",
        back_populates="trip"
    )

    parcel = relationship(
        "Parcel",
        back_populates="trip",
        uselist=False
    )
    disputes = relationship(
    "Dispute",
    back_populates="trip")


class TripLocation(Base):
    __tablename__ = "trip_locations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    trip_id = Column(
        UUID(as_uuid=True),
        ForeignKey("trips.id")
    )

    lat = Column(Numeric(10, 7))
    lng = Column(Numeric(10, 7))
    recorded_at = Column(DateTime, default=datetime.utcnow)
    # RELATIONSHIPS

    trip = relationship(
        "Trip",
        back_populates="locations"
    )
    
    
class Parcel(Base):
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

    sender_name = Column(String(100), nullable=False)

    sender_phone = Column(String(20), nullable=False)

    receiver_name = Column(String(100), nullable=False)

    receiver_phone = Column(String(20), nullable=False)

    receiver_address = Column(String(255), nullable=False)

    package_type = Column(String(50))

    weight_kg = Column(Numeric(5, 2))

    cod_amount = Column(Numeric(10, 2), default=0.0)

    pod_photo_url = Column(String(255))

    pod_signature_url = Column(String(255))

    pod_otp = Column(String(6))

    status = Column(String(50), default="pending")

    created_at = Column(DateTime, default=datetime.utcnow)

    # RELATIONSHIPS

    trip = relationship(
        "Trip",
        back_populates="parcel"
    )