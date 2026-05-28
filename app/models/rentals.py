import uuid
from datetime import datetime,timezone

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, Numeric, String, Text, Boolean
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from app.core.enums import InspectionType
from app.core.database import Base


class Rental(Base):
    __tablename__ = "rentals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_id = Column(UUID(as_uuid=True), ForeignKey("vehicles.id"))
    renter_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

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
    agreement_url = Column(String(255))
    total_fare = Column(Numeric(10, 2))

    no_of_seats = Column(Integer, nullable=False)
    date_of_booking = Column(DateTime(timezone=True), default=datetime.utcnow)
    return_date = Column(DateTime(timezone=True), default=datetime.utcnow)
    no_of_days = Column(Integer, nullable=False)

    rating = Column(Integer, nullable=True)
    comments = Column(Text, nullable=True)
    cancel_reason = Column(Text, nullable=True)
    is_cancelled = Column(Boolean, default=False)
    cancelled_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    vehicle = relationship("Vehicle", back_populates="rentals")
    renter = relationship("User", foreign_keys=[renter_id], back_populates="rentals_as_renter")
    owner = relationship("User", foreign_keys=[owner_id], back_populates="rentals_as_owner")
    inspections = relationship("RentalInspection", back_populates="rental")
    payments = relationship("Payment", back_populates="rental")
    disputes = relationship("Dispute", back_populates="rental")
    ratings = relationship("Rating", back_populates="rental", cascade="all, delete-orphan")


class RentalInspection(Base):
    __tablename__ = "rental_inspections"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rental_id = Column(UUID(as_uuid=True), ForeignKey("rentals.id"), nullable=False)
    inspection_type = Column(Enum(InspectionType), nullable=False)
    fuel_level = Column(Numeric(5, 2), nullable=True)
    odometer_reading = Column(Integer, nullable=True)
    damage_notes = Column(Text, nullable=True)
    photo_urls = Column(JSONB, nullable=True)
    video_url = Column(String(255), nullable=True)
    inspector_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    inspected_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    rental = relationship("Rental", back_populates="inspections")
    inspector = relationship("User", foreign_keys=[inspector_user_id], back_populates="rental_inspections")