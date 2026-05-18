from datetime import datetime

from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Boolean,
    Text,
    DateTime,
    Integer,
    Numeric,
    ForeignKey,
    Enum as SqlEnum,
)

from core.database import Base
from core.enums import (
    RideType,
    RideStatus,
    PaymentMethod,
    PaymentStatus,
)


class Ride(Base):
    __tablename__ = "rides"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)

    customer_id = Column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    driver_id = Column(
        BigInteger,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    ride_type = Column(SqlEnum(RideType), nullable=False)

    pickup_latitude = Column(Numeric(10, 8), nullable=False)
    pickup_longitude = Column(Numeric(11, 8), nullable=False)
    pickup_address = Column(Text, nullable=False)
    pickup_landmark = Column(Text, nullable=True)

    drop_latitude = Column(Numeric(10, 8), nullable=True)
    drop_longitude = Column(Numeric(11, 8), nullable=True)
    drop_address = Column(Text, nullable=True)

    is_scheduled = Column(Boolean, default=False, nullable=False)
    scheduled_for = Column(DateTime, nullable=True)

    base_fare = Column(Numeric(10, 2), nullable=True)
    distance_fare = Column(Numeric(10, 2), nullable=True)
    time_fare = Column(Numeric(10, 2), nullable=True)

    surge_multiplier = Column(Numeric(4, 2), default=1.0, nullable=False)
    surge_contribution = Column(Numeric(10, 2), default=0, nullable=False)

    waiting_charges = Column(Numeric(10, 2), default=0, nullable=False)
    toll_charges = Column(Numeric(10, 2), default=0, nullable=False)
    discount_amount = Column(Numeric(10, 2), default=0, nullable=False)

    promo_code = Column(String(50), nullable=True)

    total_fare = Column(Numeric(10, 2), nullable=False)
    final_fare = Column(Numeric(10, 2), nullable=True)

    status = Column(
        SqlEnum(RideStatus),
        default=RideStatus.SEARCHING,
        nullable=False,
    )

    cancellation_reason = Column(Text, nullable=True)

    cancelled_by = Column(
        BigInteger,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    pickup_otp = Column(String(6), nullable=True)
    otp_verified_at = Column(DateTime, nullable=True)

    driver_assigned_at = Column(DateTime, nullable=True)
    driver_arrived_at = Column(DateTime, nullable=True)
    trip_started_at = Column(DateTime, nullable=True)
    trip_ended_at = Column(DateTime, nullable=True)

    scheduled_ride_processed_at = Column(DateTime, nullable=True)

    actual_distance_km = Column(Numeric(10, 2), nullable=True)
    actual_duration_minutes = Column(Integer, nullable=True)
    route_polyline = Column(Text, nullable=True)

    payment_method = Column(SqlEnum(PaymentMethod), nullable=False)

    payment_status = Column(
        SqlEnum(PaymentStatus),
        default=PaymentStatus.PENDING,
        nullable=False,
    )

    payment_id = Column(
        BigInteger,
        ForeignKey("payments.id", ondelete="SET NULL"),
        nullable=True,
    )

    customer_rating = Column(Numeric(2, 1), nullable=True)
    customer_feedback = Column(Text, nullable=True)

    driver_rating = Column(Numeric(2, 1), nullable=True)
    driver_feedback = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )