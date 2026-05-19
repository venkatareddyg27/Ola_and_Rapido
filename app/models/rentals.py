# rentals.py

import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String
)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models.base import Base


class Rental(Base):
    __tablename__ = "rentals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    vehicle_id = Column(
        UUID(as_uuid=True),
        ForeignKey("vehicles.id")
    )

    renter_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id")
    )

    owner_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id")
    )
    pickup_time = Column(DateTime)
    drop_time = Column(DateTime)
    pickup_lat = Column(Numeric(10, 7))
    pickup_lng = Column(Numeric(10, 7))
    drop_lat = Column(Numeric(10, 7))
    drop_lng = Column(Numeric(10, 7))
    status = Column(String(50))
    daily_rate = Column(Numeric(10, 2))
    per_km_rate = Column(Numeric(10, 2))
    deposit_amount = Column(Numeric(10, 2))
    included_km = Column(Integer)
    deposit_status = Column(String(50))
    aggrement_url = Column(String(255))
    total_fare = Column(Numeric(10, 2))
    created_at = Column(DateTime, default=datetime.utcnow)

    # RELATIONSHIPS

    vehicle = relationship(
        "Vehicle",
        back_populates="rentals"
    )

    renter = relationship(
        "User",
        foreign_keys=[renter_id],
        back_populates="rentals_as_renter"
    )

    owner = relationship(
        "User",
        foreign_keys=[owner_id],
        back_populates="rentals_as_owner"
    )

    inspections = relationship(
        "RentalInspection",
        back_populates="rental"
    )

    payments = relationship(
        "Payment",
        back_populates="rental"
    )
    
    disputes = relationship(
    "Dispute",
    back_populates="rental")