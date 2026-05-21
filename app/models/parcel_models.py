from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    BigInteger,
    String,
    Text,
    Integer,
    DateTime,
    ForeignKey,
    Numeric,
    CheckConstraint,
    Enum as SqlEnum,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.enums import (
    ParcelStatus,
    ParcelType,
    ParcelPriority,
    ProofType,
    DeliveryAttemptStatus,
    PaymentStatus,
    FeedbackType,
)


class Parcel(Base):
    __tablename__ = "parcels"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    sender_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    receiver_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    driver_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)

    pickup_address: Mapped[str] = mapped_column(Text, nullable=False)
    pickup_lat: Mapped[Decimal] = mapped_column(Numeric(10, 7), nullable=False)
    pickup_lng: Mapped[Decimal] = mapped_column(Numeric(10, 7), nullable=False)

    delivery_address: Mapped[str] = mapped_column(Text, nullable=False)
    delivery_lat: Mapped[Decimal] = mapped_column(Numeric(10, 7), nullable=False)
    delivery_lng: Mapped[Decimal] = mapped_column(Numeric(10, 7), nullable=False)

    parcel_type: Mapped[ParcelType] = mapped_column(
        SqlEnum(ParcelType, name="parcel_type_enum"),
       default=ParcelType.SMALL,
        nullable=False,
    )

    priority: Mapped[ParcelPriority] = mapped_column(
        SqlEnum(ParcelPriority, name="parcel_priority_enum"),
        default=ParcelPriority.NORMAL,
        nullable=False,
    )

    status: Mapped[ParcelStatus] = mapped_column(
        SqlEnum(ParcelStatus, name="parcel_status_enum"),
        default=ParcelStatus.CREATED,
        nullable=False,
    )

    requested_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    picked_up_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    delivered_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    cancelled_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    items = relationship("ParcelItem", back_populates="parcel", cascade="all, delete-orphan")
    tracking = relationship("ParcelTracking", back_populates="parcel", cascade="all, delete-orphan")
    status_history = relationship("ParcelStatusHistory", back_populates="parcel", cascade="all, delete-orphan")
    proofs = relationship("ParcelProof", back_populates="parcel", cascade="all, delete-orphan")
    delivery_attempts = relationship("ParcelDeliveryAttempt", back_populates="parcel", cascade="all, delete-orphan")
    pricing = relationship("ParcelPricing", back_populates="parcel", uselist=False, cascade="all, delete-orphan")
    feedback = relationship("ParcelFeedback", back_populates="parcel", cascade="all, delete-orphan")


class ParcelItem(Base):
    __tablename__ = "parcel_items"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    parcel_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("parcels.id", ondelete="CASCADE"),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    weight_kg: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    declared_value: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    parcel = relationship("Parcel", back_populates="items")


class ParcelTracking(Base):
    __tablename__ = "parcel_tracking"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    parcel_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("parcels.id", ondelete="CASCADE"),
        nullable=False,
    )

    latitude: Mapped[Decimal] = mapped_column(Numeric(10, 7), nullable=False)
    longitude: Mapped[Decimal] = mapped_column(Numeric(10, 7), nullable=False)
    location_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)

    recorded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    parcel = relationship("Parcel", back_populates="tracking")


class ParcelStatusHistory(Base):
    __tablename__ = "parcel_status_history"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    parcel_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("parcels.id", ondelete="CASCADE"),
        nullable=False,
    )

    old_status: Mapped[ParcelStatus | None] = mapped_column(
        SqlEnum(ParcelStatus, name="parcel_status_enum"),
        nullable=True,
    )

    new_status: Mapped[ParcelStatus] = mapped_column(
        SqlEnum(ParcelStatus, name="parcel_status_enum"),
        nullable=False,
    )

    changed_by: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    changed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    parcel = relationship("Parcel", back_populates="status_history")


class ParcelProof(Base):
    __tablename__ = "parcel_proofs"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    parcel_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("parcels.id", ondelete="CASCADE"),
        nullable=False,
    )

    proof_type: Mapped[ProofType] = mapped_column(
        SqlEnum(ProofType, name="proof_type_enum"),
        nullable=False,
    )

    proof_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    otp_code: Mapped[str | None] = mapped_column(String(20), nullable=True)
    signed_by: Mapped[str | None] = mapped_column(String(150), nullable=True)

    uploaded_by: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    parcel = relationship("Parcel", back_populates="proofs")


class ParcelDeliveryAttempt(Base):
    __tablename__ = "parcel_delivery_attempts"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    parcel_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("parcels.id", ondelete="CASCADE"),
        nullable=False,
    )

    attempt_number: Mapped[int] = mapped_column(Integer, nullable=False)

    status: Mapped[DeliveryAttemptStatus] = mapped_column(
        SqlEnum(DeliveryAttemptStatus, name="delivery_attempt_status_enum"),
        nullable=False,
    )

    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    attempted_by: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    attempted_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    next_attempt_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    parcel = relationship("Parcel", back_populates="delivery_attempts")


class ParcelPricing(Base):
    __tablename__ = "parcel_pricing"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    parcel_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("parcels.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    base_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0)
    distance_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0)
    weight_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0)
    priority_fee: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0)
    discount_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0)
    tax_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0)

    total_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(10), default="INR")

    payment_status: Mapped[PaymentStatus] = mapped_column(
        SqlEnum(PaymentStatus, name="parcel_payment_status_enum"),
        default=PaymentStatus.PENDING,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    parcel = relationship("Parcel", back_populates="pricing")


class ParcelFeedback(Base):
    __tablename__ = "parcel_feedback"

    __table_args__ = (
        CheckConstraint("rating >= 1 AND rating <= 5", name="check_parcel_feedback_rating"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    parcel_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("parcels.id", ondelete="CASCADE"),
        nullable=False,
    )

    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)

    feedback_type: Mapped[FeedbackType | None] = mapped_column(
        SqlEnum(FeedbackType, name="parcel_feedback_type_enum"),
        nullable=True,
    )

    rating: Mapped[int | None] = mapped_column(Integer, nullable=True)
    message: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    parcel = relationship("Parcel", back_populates="feedback")