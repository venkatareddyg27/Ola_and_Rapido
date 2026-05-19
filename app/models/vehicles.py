import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    Integer,
    Enum,
    ForeignKey,
    DateTime
)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models.base import Base
from core.enums import (
    VehicleCategory,
    VehicleStatus,
    VehiclePhotoAngle
)


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    owner_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id")
    )

    make = Column(String(50))
    model = Column(String(50))

    year = Column(Integer)

    registration_number = Column(
        String(50),
        unique=True
    )

    category = Column(Enum(VehicleCategory))

    status = Column(
        Enum(VehicleStatus),
        default=VehicleStatus.PENDING
    )

    created_at = Column(DateTime, default=datetime.utcnow)
    sitting_capacity = Column(Integer)
    fuel_type = Column(String(50))
    colour = Column(String(50))
    # RELATIONSHIPS

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
        back_populates="vehicle"
    )


class VehiclePhoto(Base):
    __tablename__ = "vehicle_photos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    vehicle_id = Column(
        UUID(as_uuid=True),
        ForeignKey("vehicles.id")
    )

    photo_url = Column(String(255))

    angle = Column(Enum(VehiclePhotoAngle))
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    # RELATIONSHIPS

    vehicle = relationship(
        "Vehicle",
        back_populates="photos"
    )