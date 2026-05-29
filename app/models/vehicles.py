import uuid
from datetime import datetime

from sqlalchemy import Column, String, Integer, Enum, ForeignKey, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.core.enums import VehicleCategory, VehicleStatus, VehiclePhotoAngle


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    make = Column(String(50), nullable=True)
    model = Column(String(50), nullable=False)
    year = Column(Integer, nullable=False)

    registration_number = Column(String(50), unique=True, nullable=False)

    category = Column(Enum(VehicleCategory), nullable=False)
    status = Column(Enum(VehicleStatus), default=VehicleStatus.PENDING, nullable=False)

    sitting_capacity = Column(Integer, nullable=False)
    fuel_type = Column(String(50), nullable=True)
    colour = Column(String(50), nullable=True)

    daily_rate = Column(Float, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship(
        "User",
        back_populates="owned_vehicles"
    )

    photos = relationship(
        "VehiclePhoto",
        back_populates="vehicle",
        cascade="all, delete-orphan"
    )

    rentals = relationship(
        "Rental",
        back_populates="vehicle"
    )

    drivers = relationship(
        "DriverProfile",
        back_populates="vehicle",
        foreign_keys="DriverProfile.vehicle_id"
    )

    documents = relationship(
        "VehicleDocument",
        back_populates="vehicle",
        cascade="all, delete-orphan"
    )

    trip_invoices = relationship(
        "TripInvoice",
        back_populates="vehicle",
        cascade="all, delete-orphan"
    )


class VehiclePhoto(Base):
    __tablename__ = "vehicle_photos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    vehicle_id = Column(
        UUID(as_uuid=True),
        ForeignKey("vehicles.id"),
        nullable=False
    )

    photo_url = Column(String(255), nullable=False)
    angle = Column(Enum(VehiclePhotoAngle), nullable=False)

    uploaded_at = Column(DateTime, default=datetime.utcnow)

    vehicle = relationship(
        "Vehicle",
        back_populates="photos"
    )


class VehicleDocument(Base):
    __tablename__ = "vehicle_documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    vehicle_id = Column(
        UUID(as_uuid=True),
        ForeignKey("vehicles.id"),
        nullable=False
    )

    document_type = Column(String(100), nullable=False)
    document_url = Column(String(500), nullable=False)
    verification_status = Column(String(50), default="pending")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    vehicle = relationship(
        "Vehicle",
        back_populates="documents"
    )