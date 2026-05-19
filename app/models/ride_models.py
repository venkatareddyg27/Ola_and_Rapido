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
    RideStatus,
    RideType,
    PaymentStatus,
    FeedbackType,
    DiscountType,
    EmergencyAlertType,
    EmergencyAlertStatus,
)


class Ride(Base):
    __tablename__ = "rides"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    rider_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    driver_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    vehicle_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)

    pickup_address: Mapped[str] = mapped_column(Text, nullable=False)
    pickup_lat: Mapped[Decimal] = mapped_column(Numeric(10, 7), nullable=False)
    pickup_lng: Mapped[Decimal] = mapped_column(Numeric(10, 7), nullable=False)

    dropoff_address: Mapped[str] = mapped_column(Text, nullable=False)
    dropoff_lat: Mapped[Decimal] = mapped_column(Numeric(10, 7), nullable=False)
    dropoff_lng: Mapped[Decimal] = mapped_column(Numeric(10, 7), nullable=False)

    ride_type: Mapped[RideType | None] = mapped_column(
        SqlEnum(RideType, name="ride_type_enum"),
        nullable=True,
    )

    status: Mapped[RideStatus] = mapped_column(
        SqlEnum(RideStatus, name="ride_status_enum"),
        default=RideStatus.REQUESTED,
        nullable=False,
    )

    requested_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    accepted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    cancelled_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    stops = relationship("RideStop", back_populates="ride", cascade="all, delete-orphan")
    status_history = relationship("RideStatusHistory", back_populates="ride", cascade="all, delete-orphan")
    fare = relationship("RideFare", back_populates="ride", uselist=False, cascade="all, delete-orphan")
    ratings = relationship("RideRating", back_populates="ride", cascade="all, delete-orphan")
    feedback = relationship("RideFeedback", back_populates="ride", cascade="all, delete-orphan")
    cancellation = relationship("RideCancellation", back_populates="ride", uselist=False, cascade="all, delete-orphan")
    route_tracking = relationship("RideRouteTracking", back_populates="ride", cascade="all, delete-orphan")
    promotions = relationship("RidePromotion", back_populates="ride", cascade="all, delete-orphan")
    emergency_alerts = relationship("RideEmergencyAlert", back_populates="ride", cascade="all, delete-orphan")


class RideStop(Base):
    __tablename__ = "ride_stops"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    ride_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("rides.id", ondelete="CASCADE"),
        nullable=False,
    )

    stop_order: Mapped[int] = mapped_column(Integer, nullable=False)
    address: Mapped[str] = mapped_column(Text, nullable=False)
    latitude: Mapped[Decimal] = mapped_column(Numeric(10, 7), nullable=False)
    longitude: Mapped[Decimal] = mapped_column(Numeric(10, 7), nullable=False)

    reached_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    ride = relationship("Ride", back_populates="stops")


class RideStatusHistory(Base):
    __tablename__ = "ride_status_history"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    ride_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("rides.id", ondelete="CASCADE"),
        nullable=False,
    )

    old_status: Mapped[RideStatus | None] = mapped_column(
        SqlEnum(RideStatus, name="ride_status_enum"),
        nullable=True,
    )
    new_status: Mapped[RideStatus] = mapped_column(
        SqlEnum(RideStatus, name="ride_status_enum"),
        nullable=False,
    )

    changed_by: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    changed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    ride = relationship("Ride", back_populates="status_history")


class RideFare(Base):
    __tablename__ = "ride_fares"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    ride_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("rides.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    base_fare: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0)
    distance_fare: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0)
    time_fare: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0)
    surge_multiplier: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=1.00)
    discount_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0)
    tax_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0)

    total_fare: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(10), default="INR")

    payment_status: Mapped[PaymentStatus] = mapped_column(
        SqlEnum(PaymentStatus, name="payment_status_enum"),
        default=PaymentStatus.PENDING,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    ride = relationship("Ride", back_populates="fare")


class RideRating(Base):
    __tablename__ = "ride_ratings"

    __table_args__ = (
        CheckConstraint("rating >= 1 AND rating <= 5", name="check_rating_between_1_and_5"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    ride_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("rides.id", ondelete="CASCADE"),
        nullable=False,
    )

    rated_by: Mapped[int] = mapped_column(BigInteger, nullable=False)
    rated_to: Mapped[int] = mapped_column(BigInteger, nullable=False)

    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    review: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    ride = relationship("Ride", back_populates="ratings")


class RideFeedback(Base):
    __tablename__ = "ride_feedback"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    ride_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("rides.id", ondelete="CASCADE"),
        nullable=False,
    )

    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)

    feedback_type: Mapped[FeedbackType | None] = mapped_column(
        SqlEnum(FeedbackType, name="feedback_type_enum"),
        nullable=True,
    )

    message: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    ride = relationship("Ride", back_populates="feedback")


class RideCancellation(Base):
    __tablename__ = "ride_cancellations"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    ride_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("rides.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    cancelled_by: Mapped[int] = mapped_column(BigInteger, nullable=False)
    reason: Mapped[str | None] = mapped_column(String(255), nullable=True)
    cancellation_fee: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0)
    cancelled_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    ride = relationship("Ride", back_populates="cancellation")


class RideRouteTracking(Base):
    __tablename__ = "ride_route_tracking"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    ride_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("rides.id", ondelete="CASCADE"),
        nullable=False,
    )

    latitude: Mapped[Decimal] = mapped_column(Numeric(10, 7), nullable=False)
    longitude: Mapped[Decimal] = mapped_column(Numeric(10, 7), nullable=False)
    speed: Mapped[Decimal | None] = mapped_column(Numeric(6, 2), nullable=True)
    heading: Mapped[Decimal | None] = mapped_column(Numeric(6, 2), nullable=True)

    recorded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    ride = relationship("Ride", back_populates="route_tracking")


class RidePromotion(Base):
    __tablename__ = "ride_promotions"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    ride_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("rides.id", ondelete="CASCADE"),
        nullable=False,
    )

    promotion_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    promo_code: Mapped[str | None] = mapped_column(String(50), nullable=True)

    discount_type: Mapped[DiscountType | None] = mapped_column(
        SqlEnum(DiscountType, name="discount_type_enum"),
        nullable=True,
    )

    discount_value: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    applied_amount: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    applied_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    ride = relationship("Ride", back_populates="promotions")


class RideEmergencyAlert(Base):
    __tablename__ = "ride_emergency_alerts"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    ride_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("rides.id", ondelete="CASCADE"),
        nullable=False,
    )

    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)

    alert_type: Mapped[EmergencyAlertType] = mapped_column(
        SqlEnum(EmergencyAlertType, name="emergency_alert_type_enum"),
        default=EmergencyAlertType.SOS,
        nullable=False,
    )

    message: Mapped[str | None] = mapped_column(Text, nullable=True)
    latitude: Mapped[Decimal | None] = mapped_column(Numeric(10, 7), nullable=True)
    longitude: Mapped[Decimal | None] = mapped_column(Numeric(10, 7), nullable=True)

    status: Mapped[EmergencyAlertStatus] = mapped_column(
        SqlEnum(EmergencyAlertStatus, name="emergency_alert_status_enum"),
        default=EmergencyAlertStatus.ACTIVE,
        nullable=False,
    )

    triggered_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    ride = relationship("Ride", back_populates="emergency_alerts")