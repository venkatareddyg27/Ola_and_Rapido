from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    Text,
    Boolean,
    DateTime,
    ForeignKey,
    Numeric,
    BigInteger,
    Integer,
    Enum as SqlEnum
)

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from app.core.database import Base
from app.core.enums import VehicleType, FuelType, TransmissionType, VehicleVerificationStatus


# =========================================================
# VEHICLE MODEL
# =========================================================
class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(BigInteger, primary_key=True, index=True)

    owner_id = Column(
        BigInteger,
        ForeignKey("users.id"),
        nullable=False
    )

    vehicle_type = Column(
        SqlEnum(VehicleType),
        nullable=False
    )

    brand = Column(String(100), nullable=False)

    model = Column(String(100), nullable=False)

    year = Column(Integer, nullable=False)

    registration_number = Column(
        String(50),
        unique=True,
        nullable=False
    )

    color = Column(String(50))

    fuel_type = Column(
        SqlEnum(FuelType),
        nullable=False
    )

    transmission_type = Column(
        SqlEnum(TransmissionType),
        nullable=False
    )

    seating_capacity = Column(Integer)

    description = Column(Text)

    price_per_day = Column(
        Numeric(10, 2),
        nullable=False
    )

    is_available = Column(
        Boolean,
        default=True
    )

    verification_status = Column(
        SqlEnum(VehicleVerificationStatus),
        default=VehicleVerificationStatus.PENDING
    )

    created_at = Column(
        DateTime,
        default=func.now()
    )

    updated_at = Column(
        DateTime,
        default=func.now(),
        onupdate=func.now()
    )


# =========================================================
# VEHICLE DOCUMENTS
# =========================================================

class VehicleDocument(Base):
    __tablename__ = "vehicle_documents"

    id = Column(BigInteger, primary_key=True, index=True)

    vehicle_id = Column(
        BigInteger,
        ForeignKey("vehicles.id"),
        nullable=False
    )

    rc_document_url = Column(Text)

    insurance_document_url = Column(Text)

    pollution_certificate_url = Column(Text)

    driving_license_url = Column(Text)

    is_verified = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime,
        default=func.now()
    )


# =========================================================
# VEHICLE INSURANCE
# =========================================================

class VehicleInsurance(Base):
    __tablename__ = "vehicle_insurance"

    id = Column(BigInteger, primary_key=True, index=True)

    vehicle_id = Column(
        BigInteger,
        ForeignKey("vehicles.id"),
        nullable=False
    )

    provider_name = Column(String(255))

    policy_number = Column(String(255))

    valid_from = Column(DateTime)

    valid_till = Column(DateTime)

    insurance_amount = Column(
        Numeric(12, 2)
    )

    created_at = Column(
        DateTime,
        default=func.now()
    )


# =========================================================
# VEHICLE MAINTENANCE LOGS
# =========================================================

class VehicleMaintenanceLog(Base):
    __tablename__ = "vehicle_maintenance_logs"

    id = Column(BigInteger, primary_key=True, index=True)

    vehicle_id = Column(
        BigInteger,
        ForeignKey("vehicles.id"),
        nullable=False
    )

    title = Column(String(255))

    description = Column(Text)

    maintenance_cost = Column(
        Numeric(10, 2)
    )

    maintenance_date = Column(DateTime)

    next_service_due = Column(DateTime)

    created_at = Column(
        DateTime,
        default=func.now()
    )


# =========================================================
# VEHICLE LISTINGS
# =========================================================

class VehicleListing(Base):
    __tablename__ = "vehicle_listings"

    id = Column(BigInteger, primary_key=True, index=True)

    vehicle_id = Column(
        BigInteger,
        ForeignKey("vehicles.id"),
        nullable=False
    )

    title = Column(String(255))

    description = Column(Text)

    city = Column(String(100))

    price_per_hour = Column(
        Numeric(10, 2)
    )

    minimum_booking_hours = Column(Integer)

    is_active = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime,
        default=func.now()
    )


# =========================================================
# VEHICLE IMAGES
# =========================================================

class VehicleImage(Base):
    __tablename__ = "vehicle_images"

    id = Column(BigInteger, primary_key=True, index=True)

    vehicle_id = Column(
        BigInteger,
        ForeignKey("vehicles.id"),
        nullable=False
    )

    image_url = Column(Text, nullable=False)

    is_primary = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime,
        default=func.now()
    )


# =========================================================
# VEHICLE FEATURES
# =========================================================

class VehicleFeature(Base):
    __tablename__ = "vehicle_features"

    id = Column(BigInteger, primary_key=True, index=True)

    vehicle_id = Column(
        BigInteger,
        ForeignKey("vehicles.id"),
        nullable=False
    )

    feature_name = Column(String(255))

    created_at = Column(
        DateTime,
        default=func.now()
    )


# =========================================================
# VEHICLE TRACKING DEVICES
# =========================================================

class VehicleTrackingDevice(Base):
    __tablename__ = "vehicle_tracking_devices"

    id = Column(BigInteger, primary_key=True, index=True)

    vehicle_id = Column(
        BigInteger,
        ForeignKey("vehicles.id"),
        nullable=False
    )

    device_imei = Column(
        String(255),
        unique=True
    )

    provider_name = Column(String(255))

    installed_at = Column(DateTime)

    is_active = Column(
        Boolean,
        default=True
    )


# =========================================================
# VEHICLE DAMAGE REPORTS
# =========================================================

class VehicleDamageReport(Base):
    __tablename__ = "vehicle_damage_reports"

    id = Column(BigInteger, primary_key=True, index=True)

    vehicle_id = Column(
        BigInteger,
        ForeignKey("vehicles.id"),
        nullable=False
    )

    reported_by = Column(
        BigInteger,
        ForeignKey("users.id")
    )

    damage_description = Column(Text)

    damage_images = Column(JSONB)

    estimated_repair_cost = Column(
        Numeric(10, 2)
    )

    reported_at = Column(
        DateTime,
        default=func.now()
    )


# =========================================================
# VEHICLE AVAILABILITY CALENDAR
# =========================================================

class VehicleAvailabilityCalendar(Base):
    __tablename__ = "vehicle_availability_calendar"

    id = Column(BigInteger, primary_key=True, index=True)

    vehicle_id = Column(
        BigInteger,
        ForeignKey("vehicles.id"),
        nullable=False
    )

    available_from = Column(DateTime)

    available_to = Column(DateTime)

    is_available = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime,
        default=func.now()
    )