from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    Date,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Numeric,
    String,
    Text,
)

from sqlalchemy.sql import func

from app.core.database import Base

from app.core.enums import (
    AttendanceStatus,
    DriverDocumentType,
    DriverStatus,
    OnlineStatus,
    PayoutMethod,
    PayoutStatus,
    PenaltyStatus,
    ShiftStatus,
    VerificationStatus,
)


class DriverProfile(Base):
    __tablename__ = "driver_profiles"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    license_number = Column(String(100), nullable=False)
    license_expiry = Column(Date, nullable=False)
    current_vehicle_id = Column(BigInteger, nullable=True)
    driver_rating = Column(Numeric(3, 2), default=0)
    total_rides = Column(BigInteger, default=0)
    online_status = Column(Enum(OnlineStatus), default=OnlineStatus.OFFLINE)
    status = Column(Enum(DriverStatus), default=DriverStatus.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class DriverDocument(Base):
    __tablename__ = "driver_documents"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    document_type = Column(Enum(DriverDocumentType), nullable=False)
    document_url = Column(Text, nullable=False)
    verification_status = Column(Enum(VerificationStatus), default=VerificationStatus.PENDING)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())


class DriverLocation(Base):
    __tablename__ = "driver_locations"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    heading = Column(Float, nullable=True)
    speed = Column(Float, nullable=True)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())


class DriverBankAccount(Base):
    __tablename__ = "driver_bank_accounts"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    account_holder_name = Column(String(255), nullable=False)
    bank_name = Column(String(255), nullable=False)
    account_number = Column(String(100), nullable=False)
    ifsc_code = Column(String(20), nullable=False)
    upi_id = Column(String(255), nullable=True)
    is_primary = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class DriverEarning(Base):
    __tablename__ = "driver_earnings"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    ride_id = Column(BigInteger, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    commission = Column(Numeric(10, 2), nullable=False)
    payout_status = Column(Enum(PayoutStatus), default=PayoutStatus.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class DriverPayout(Base):
    __tablename__ = "driver_payouts"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    payout_amount = Column(Numeric(10, 2), nullable=False)
    payout_method = Column(Enum(PayoutMethod), nullable=False)
    payout_status = Column(Enum(PayoutStatus), default=PayoutStatus.PENDING)
    processed_at = Column(DateTime(timezone=True), nullable=True)


class DriverShift(Base):
    __tablename__ = "driver_shifts"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    shift_start = Column(DateTime(timezone=True), nullable=False)
    shift_end = Column(DateTime(timezone=True), nullable=True)
    status = Column(Enum(ShiftStatus), default=ShiftStatus.STARTED)


class DriverOnlineSession(Base):
    __tablename__ = "driver_online_sessions"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    login_time = Column(DateTime(timezone=True), nullable=False)
    logout_time = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)


class DriverRating(Base):
    __tablename__ = "driver_ratings"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    customer_id = Column(BigInteger, nullable=False)
    ride_id = Column(BigInteger, nullable=False)
    rating = Column(Numeric(2, 1), nullable=False)
    review = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class DriverPenalty(Base):
    __tablename__ = "driver_penalties"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    reason = Column(Text, nullable=False)
    penalty_amount = Column(Numeric(10, 2), nullable=False)
    status = Column(Enum(PenaltyStatus), default=PenaltyStatus.ACTIVE)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class DriverIncentive(Base):
    __tablename__ = "driver_incentives"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    incentive_title = Column(String(255), nullable=False)
    incentive_amount = Column(Numeric(10, 2), nullable=False)
    achieved = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class DriverAttendance(Base):
    __tablename__ = "driver_attendance"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    attendance_date = Column(Date, nullable=False)
    status = Column(Enum(AttendanceStatus), default=AttendanceStatus.PRESENT)
    created_at = Column(DateTime(timezone=True), server_default=func.now())