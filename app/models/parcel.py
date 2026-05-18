# app/models/parcel.py

from app.core.enums import (
    PackageType,WeightTier,ParcelStatus)
import uuid

from sqlalchemy import (
    Column,
    String,
    Text,
    Boolean,
    DateTime,
    ForeignKey,
    Numeric,
    Enum,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func

from app.core.database import Base


# -------------------------
# MODEL
# -------------------------

class Parcel(Base):
    __tablename__ = "parcels"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Booking Reference
    booking_reference = Column(String(20), unique=True, nullable=False)

    # Foreign Keys
    sender_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    receiver_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True
    )

    driver_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True
    )

    # Package Details
    package_type = Column(
        Enum(PackageType),
        nullable=True
    )

    weight_tier = Column(
        Enum(WeightTier),
        nullable=True
    )

    dimensions = Column(JSONB, nullable=True)

    description = Column(Text, nullable=True)

    is_fragile = Column(Boolean, default=False)

    # Pickup Details
    pickup_address = Column(Text, nullable=False)

    pickup_latitude = Column(
        Numeric(10, 7),
        nullable=False
    )

    pickup_longitude = Column(
        Numeric(10, 7),
        nullable=False
    )

    pickup_contact_name = Column(
        String(255),
        nullable=True
    )

    pickup_contact_phone = Column(
        String(15),
        nullable=True
    )

    pickup_instruction = Column(
        Text,
        nullable=True
    )

    # Delivery Details
    delivery_address = Column(Text, nullable=False)

    delivery_latitude = Column(
        Numeric(10, 7),
        nullable=False
    )

    delivery_longitude = Column(
        Numeric(10, 7),
        nullable=False
    )

    receiver_name = Column(
        String(255),
        nullable=True
    )

    receiver_phone = Column(
        String(15),
        nullable=True
    )

    # COD
    is_cod = Column(Boolean, default=False)

    cod_amount = Column(
        Numeric(10, 2),
        nullable=True
    )

    cod_collected = Column(
        Boolean,
        default=False
    )

    # Proofs
    proof_of_pickup_url = Column(Text, nullable=True)

    proof_of_delivery_url = Column(Text, nullable=True)

    proof_of_delivery_signature = Column(
        Text,
        nullable=True
    )

    # Status
    status = Column(
        Enum(ParcelStatus),
        default=ParcelStatus.pending_pickup
    )

    # Time Tracking
    pickup_photo_taken_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    picked_up_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    delivered_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    expected_delivery_time = Column(
        DateTime(timezone=True),
        nullable=True
    )

    # Fare Details
    base_fare = Column(
        Numeric(10, 2),
        nullable=True
    )

    distance_fare = Column(
        Numeric(10, 2),
        nullable=True
    )

    cod_fee = Column(
        Numeric(10, 2),
        default=0
    )

    total_fare = Column(
        Numeric(10, 2),
        nullable=True
    )

    # Payment
    payment_method = Column(
        String(20),
        nullable=True
    )

    payment_status = Column(
        String(20),
        nullable=True
    )

    # Timestamps
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )