from datetime import datetime
 
from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    String,
    Text,
    Date,
    Time,
    DateTime,
    Boolean,
    Numeric,
    ForeignKey,
    Enum as SqlEnum,
)
from sqlalchemy.dialects.postgresql import JSONB
 
from app.core.database import Base
from app.core.enums import RentalBookingStatus, DamageClaimStatus
 
 
# =========================================================
# RENTAL BOOKINGS
# =========================================================
class RentalBooking(Base):
    __tablename__ = "rental_bookings"
 
    id = Column(BigInteger, primary_key=True, index=True)
 
    customer_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    vehicle_id = Column(BigInteger, ForeignKey("vehicles.id", ondelete="CASCADE"), nullable=False)
 
    pickup_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=False)
    pickup_time = Column(Time, nullable=True)
    return_time = Column(Time, nullable=True)
 
    total_days = Column(Integer, nullable=False)
 
    pickup_location = Column(Text, nullable=True)
    return_location = Column(Text, nullable=True)
 
    daily_rate = Column(Numeric(10, 2), nullable=False)
    total_rental_amount = Column(Numeric(10, 2), nullable=False)
    security_deposit_amount = Column(Numeric(10, 2), nullable=False)
 
    km_limit_included = Column(Integer, nullable=True)
    per_km_overage_rate = Column(Numeric(10, 2), nullable=True)
 
    renter_kyc_verified_at = Column(DateTime, nullable=True)
 
    status = Column(SqlEnum(RentalBookingStatus), default=RentalBookingStatus.PENDING, nullable=False)
 
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
 
 
# =========================================================
# RENTAL EXTENSIONS
# =========================================================
class RentalExtension(Base):
    __tablename__ = "rental_extensions"
 
    id = Column(BigInteger, primary_key=True, index=True)
    booking_id = Column(BigInteger, ForeignKey("rental_bookings.id", ondelete="CASCADE"))
 
    old_end_date = Column(Date, nullable=False)
    new_end_date = Column(Date, nullable=False)
 
    extra_amount = Column(Numeric(10, 2), nullable=False)
 
    status = Column(String(20), default="pending")
 
    created_at = Column(DateTime, default=datetime.utcnow)
 
 
# =========================================================
# RENTAL TRIP LOGS
# =========================================================
class RentalTripLog(Base):
    __tablename__ = "rental_trip_logs"
 
    id = Column(BigInteger, primary_key=True, index=True)
    booking_id = Column(BigInteger, ForeignKey("rental_bookings.id", ondelete="CASCADE"))
 
    start_km = Column(Integer, nullable=False)
    end_km = Column(Integer, nullable=True)
 
    fuel_before = Column(Numeric(5, 2), nullable=True)
    fuel_after = Column(Numeric(5, 2), nullable=True)
 
    extra_km_charge = Column(Numeric(10, 2), default=0)
 
    created_at = Column(DateTime, default=datetime.utcnow)
 
 
# =========================================================
# RENTAL SECURITY DEPOSITS
# =========================================================
class RentalSecurityDeposit(Base):
    __tablename__ = "rental_security_deposits"
 
    id = Column(BigInteger, primary_key=True, index=True)
    booking_id = Column(BigInteger, ForeignKey("rental_bookings.id", ondelete="CASCADE"))
 
    deposit_amount = Column(Numeric(10, 2), nullable=False)
    refund_amount = Column(Numeric(10, 2), default=0)
    deduction_amount = Column(Numeric(10, 2), default=0)
 
    refund_status = Column(String(20), default="pending")
 
    refund_date = Column(DateTime, nullable=True)
 
    created_at = Column(DateTime, default=datetime.utcnow)
 
 
# =========================================================
# RENTAL CHECKLISTS
# =========================================================
class RentalChecklist(Base):
    __tablename__ = "rental_checklists"
 
    id = Column(BigInteger, primary_key=True, index=True)
    booking_id = Column(BigInteger, ForeignKey("rental_bookings.id", ondelete="CASCADE"))
 
    checklist_type = Column(String(20))  # pickup / return
 
    helmet_available = Column(Boolean, default=False)
    rc_available = Column(Boolean, default=False)
    insurance_available = Column(Boolean, default=False)
 
    vehicle_condition = Column(Text, nullable=True)
    customer_signature = Column(Text, nullable=True)
 
    created_at = Column(DateTime, default=datetime.utcnow)
 
 
# =========================================================
# RENTAL FUEL LOGS
# =========================================================
class RentalFuelLog(Base):
    __tablename__ = "rental_fuel_logs"
 
    id = Column(BigInteger, primary_key=True, index=True)
    booking_id = Column(BigInteger, ForeignKey("rental_bookings.id", ondelete="CASCADE"))
 
    fuel_level = Column(Numeric(5, 2), nullable=False)
    fuel_cost = Column(Numeric(10, 2), nullable=True)
 
    fuel_station = Column(String(100), nullable=True)
    receipt_image = Column(Text, nullable=True)
 
    created_at = Column(DateTime, default=datetime.utcnow)
 
 
# =========================================================
# RENTAL DAMAGE REPORTS
# =========================================================
class RentalDamageReport(Base):
    __tablename__ = "rental_damage_reports"
 
    id = Column(BigInteger, primary_key=True, index=True)
    booking_id = Column(BigInteger, ForeignKey("rental_bookings.id", ondelete="CASCADE"))
 
    damage_description = Column(Text, nullable=False)
    damage_cost = Column(Numeric(10, 2), default=0)
 
    proof_images = Column(JSONB, default=list)
 
    report_status = Column(SqlEnum(DamageClaimStatus), default=DamageClaimStatus.PENDING)
 
    created_at = Column(DateTime, default=datetime.utcnow)
 
 
# =========================================================
# RENTAL INSPECTIONS
# =========================================================
class RentalInspection(Base):
    __tablename__ = "rental_inspections"
 
    id = Column(BigInteger, primary_key=True, index=True)
    booking_id = Column(BigInteger, ForeignKey("rental_bookings.id", ondelete="CASCADE"))
 
    inspection_type = Column(String(20))  # pre / post
 
    inspected_by = Column(BigInteger, nullable=True)
 
    odometer = Column(Integer, nullable=True)
    fuel_level = Column(String(20), nullable=True)
 
    notes = Column(Text, nullable=True)
 
    images = Column(JSONB, default=list)
    video_url = Column(Text, nullable=True)
 
    completed_at = Column(DateTime, nullable=True)
 
    created_at = Column(DateTime, default=datetime.utcnow)
 