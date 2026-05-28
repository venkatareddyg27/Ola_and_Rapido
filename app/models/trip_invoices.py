from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    Numeric,
    Integer,
    DateTime,
    Enum as SqlEnum)
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.core.enums import TripType,PaymentStatus,InvoiceStatus
import uuid



class TripInvoice(Base):

    __tablename__ = "trip_invoices"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4)

    trip_id = Column(
        UUID(as_uuid=True),
        ForeignKey("trips.id", ondelete="CASCADE"),
        nullable=False,
        unique=True)

    customer_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False)

    driver_id = Column(
        UUID(as_uuid=True),
        ForeignKey("driver_profiles.id", ondelete="CASCADE"),
        nullable=False)

    vehicle_id = Column(
        UUID(as_uuid=True),
        ForeignKey("vehicles.id", ondelete="SET NULL"),
        nullable=True)

    invoice_number = Column(
        String(100),
        unique=True,
        nullable=False)

    trip_type = Column(
        SqlEnum(TripType),
        nullable=True)

    base_fare = Column(
        Numeric(10, 2),
        default=0)

    distance_km = Column(
        Numeric(10, 2),
        default=0)

    distance_charge = Column(
        Numeric(10, 2),
        default=0)

    duration_minutes = Column(
        Integer,
        default=0)

    time_charge = Column(
        Numeric(10, 2),
        default=0)

    waiting_charge = Column(
        Numeric(10, 2),
        default=0)

    surge_charge = Column(
        Numeric(10, 2),
        default=0)

    tax_amount = Column(
        Numeric(10, 2),
        default=0)

    discount_amount = Column(
        Numeric(10, 2),
        default=0)

    subtotal = Column(
        Numeric(10, 2),
        default=0)

    total_amount = Column(
        Numeric(10, 2),
        nullable=False)

    payment_method = Column(
        String(30),
        nullable=True)

    payment_status = Column(
    SqlEnum(PaymentStatus),
    default=PaymentStatus.PENDING)

    invoice_status = Column(
        SqlEnum(InvoiceStatus),
        default=InvoiceStatus.generated)

    pdf_url = Column(
        String,
        nullable=True)

    generated_at = Column(
        DateTime,
        default=datetime.utcnow)

    created_at = Column(
        DateTime,
        default=datetime.utcnow)

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow)

    trip = relationship("Trip", back_populates="invoice")
    customer = relationship(
        "User",
        back_populates="trip_invoices")

    driver = relationship(
        "DriverProfile",
        back_populates="trip_invoices")

    vehicle = relationship(
        "Vehicle",
        back_populates="trip_invoices")