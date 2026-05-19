# rentals.py
 
import uuid
from datetime import datetime
 
from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text
)


from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship
 
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship
from app.core.enums import InspectionType
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
 
class RentalInspection(Base):
    __tablename__ = "rental_inspections"
 
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rental_id = Column(
        UUID(as_uuid=True),
        ForeignKey("rentals.id"),
        nullable=False
    )

    inspection_type = Column(Enum(InspectionType), nullable=False)

    fuel_level = Column(Numeric(5, 2), nullable=True)
    odometer_reading = Column(Integer, nullable=True)

    damage_notes = Column(Text, nullable=True)
    photo_urls = Column(JSONB, nullable=True)
    video_url = Column(String(255), nullable=True)
 
    inspection_type = Column(Enum(InspectionType), nullable=False)
 
    fuel_level = Column(Numeric(5, 2), nullable=True)
    odometer_reading = Column(Integer, nullable=True)
 
    damage_notes = Column(Text, nullable=True)
    photo_urls = Column(JSONB, nullable=True)
    video_url = Column(String(255), nullable=True)
    inspector_user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    inspected_at = Column(DateTime, nullable=False)
 
    # RELATIONSHIPS
    rental = relationship(
        "Rental",
        back_populates="inspections"
    )

    inspector = relationship(
        "User",
        back_populates="rental_inspections"
    )
 
    inspector = relationship(
        "User",
        back_populates="rental_inspections"
    )
 
>>>>>>> f130a11f3e48383a0003076f2801887ee2655dd4
