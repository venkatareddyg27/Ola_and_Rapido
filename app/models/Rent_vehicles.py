import uuid
from datetime import datetime
from sqlalchemy import (Column, String,Integer,Enum,ForeignKey,DateTime,Boolean,Float,Text)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.core.enums import (VehicleCategory,VehicleStatus,VehiclePhotoAngle)

class RentedVehicle(Base):
    __tablename__ = "rented_vehicles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    make = Column(String(50), nullable=False)
    model = Column(String(50), nullable=False)
    year = Column(Integer, nullable=False)
    registration_number = Column(String(50), unique=True, nullable=False)

    category = Column(Enum(VehicleCategory), nullable=False)
    status = Column(Enum(VehicleStatus), default=VehicleStatus.PENDING)

    colour = Column(String(50))
    sitting_capacity = Column(Integer)
    fuel_type = Column(String(50))
    transmission_type = Column(String(50))
    fuel_capacity = Column(Float)
    mileage = Column(Float)
    current_odometer = Column(Integer, default=0)

    price_per_hour = Column(Float)
    price_per_day = Column(Float)
    security_deposit = Column(Float)

    ac_available = Column(Boolean, default=True)
    gps_enabled = Column(Boolean, default=False)
    bluetooth_available = Column(Boolean, default=False)
    music_system = Column(Boolean, default=False)
    sunroof = Column(Boolean, default=False)
    airbags = Column(Integer, default=2)

    boot_space = Column(String(50))
    insurance_expiry = Column(DateTime)
    pollution_expiry = Column(DateTime)
    fitness_expiry = Column(DateTime)
    permit_expiry = Column(DateTime)

    is_available = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    verification_notes = Column(Text)

    city = Column(String(100))
    state = Column(String(100))
    current_latitude = Column(Float)
    current_longitude = Column(Float)

    has_damage = Column(Boolean, default=False)
    damage_notes = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner = relationship(
        "User",
        back_populates="rented_vehicles"
    )

    photos = relationship(
        "RentedVehiclePhoto",
        back_populates="rented_vehicle",
        cascade="all, delete-orphan"
    )

    rentedVehicleDocuments = relationship(
        "RentedVehicleDocument",
        back_populates="rented_vehicle",
        cascade="all, delete-orphan"
    )

    damage_reports = relationship(
        "VehicleDamageReport",
        back_populates="rented_vehicle",
        cascade="all, delete-orphan"
    )

    availability_slots = relationship(
        "VehicleAvailability",
        back_populates="rented_vehicle",
        cascade="all, delete-orphan"
    )
class VehicleDamageReport(Base):

    __tablename__ = "vehicle_damage_reports"

    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    vehicle_id = Column(UUID(as_uuid=True),ForeignKey("rented_vehicles.id"))
    reported_by = Column(UUID(as_uuid=True),ForeignKey("users.id"))
    damage_type = Column(String(100))
    description = Column(Text)
    estimated_repair_cost = Column(Float)
    damage_photo = Column(String(500))
    status = Column(String(50), default="pending")
    created_at = Column(DateTime,default=datetime.utcnow)

## Relationships
    rented_vehicle = relationship( "RentedVehicle", back_populates="damage_reports" ) 
    reporter = relationship( "User" )

class VehicleAvailability(Base):

    __tablename__ = "vehicle_availability"
    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    vehicle_id = Column(UUID(as_uuid=True),ForeignKey("rented_vehicles.id"))
    available_from = Column(DateTime)
    available_to = Column(DateTime)
    is_booked = Column(Boolean, default=False)
    created_at = Column(DateTime,default=datetime.utcnow)

### Relationships
    rented_vehicle = relationship( "RentedVehicle", back_populates="availability_slots" )
    
    
class RentedVehiclePhoto(Base):
    __tablename__ = "rented_vehicle_photos"
    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    rented_vehicle_id = Column(UUID(as_uuid=True),ForeignKey("rented_vehicles.id"))
    photo_url = Column(String(255))
    angle = Column(Enum(VehiclePhotoAngle))
    uploaded_at = Column(DateTime,default=datetime.utcnow)
    rented_vehicle = relationship("RentedVehicle",back_populates="photos")



class RentedVehicleDocument(Base):

    __tablename__ = "rented_vehicle_documents"
    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    rented_vehicle_id = Column(UUID(as_uuid=True),ForeignKey("rented_vehicles.id"),nullable=False)
    document_type = Column(String(100),nullable=False)
    document_number = Column(String(100))
    document_url = Column(String(500),nullable=False)
    verification_status = Column(String(50),default="pending")
    rejection_reason = Column(Text)
    verified_by = Column(UUID(as_uuid=True),ForeignKey("users.id"),nullable=True)
    verified_at = Column(DateTime)
    expiry_date = Column(DateTime)
    created_at = Column(DateTime,default=datetime.utcnow)
    updated_at = Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)

    rented_vehicle = relationship("RentedVehicle",back_populates="rentedVehicleDocuments")
    verifier = relationship("User",foreign_keys=[verified_by])

