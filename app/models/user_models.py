# =========================================================
# app/models/user_models.py
# =========================================================

import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Text,
    Integer,
    Numeric,
    Enum as SqlEnum,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.core.enums import SubscriptionPlan, DriverStatus, OTPPurpose


# =========================================================
# USERS
# =========================================================

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    full_name = Column(String(255), nullable=True)
    email = Column(String(255), unique=True, nullable=True, index=True)
    mobile_number = Column(String(20), unique=True, nullable=True, index=True)

    role = Column(String(50), default="USER")
    gender = Column(String(20), nullable=True)
    profile_photo_url = Column(Text, nullable=True)

    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")
    devices = relationship("UserDevice", back_populates="user", cascade="all, delete-orphan")
    roles = relationship("UserRole", back_populates="user", cascade="all, delete-orphan")
    password_reset_tokens = relationship("PasswordResetToken", back_populates="user", cascade="all, delete-orphan")
    login_history = relationship("LoginHistory", back_populates="user", cascade="all, delete-orphan")
    blocked_users = relationship(
        "BlockedUser",
        foreign_keys="BlockedUser.user_id",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    driver_profile = relationship("DriverProfile", back_populates="user", uselist=False)
    kyc_documents = relationship("KYCDocument", back_populates="user", cascade="all, delete-orphan")
    otp_logs = relationship("OTPLog", back_populates="user", cascade="all, delete-orphan")
    customer_trips = relationship(
    "Trip",
    back_populates="customer"
)

# =========================================================
# USER SESSIONS
# =========================================================

class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    access_token = Column(Text, nullable=False)
    refresh_token = Column(Text, nullable=False)
    device_info = Column(String(255), nullable=True)
    ip_address = Column(String(100), nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="sessions")


# =========================================================
# USER DEVICES
# =========================================================

class UserDevice(Base):
    __tablename__ = "user_devices"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    device_id = Column(String(255), nullable=False)
    device_type = Column(String(50), nullable=False)
    fcm_token = Column(Text, nullable=True)
    app_version = Column(String(20), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="devices")


# =========================================================
# USER ROLES
# =========================================================

class UserRole(Base):
    __tablename__ = "user_roles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    role_name = Column(String(100), nullable=False)
    assigned_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="roles")


# =========================================================
# USER PERMISSIONS
# =========================================================

class UserPermission(Base):
    __tablename__ = "user_permissions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    permission_name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    role_permissions = relationship("RolePermission", back_populates="permission", cascade="all, delete-orphan")


# =========================================================
# ROLE PERMISSIONS
# =========================================================

class RolePermission(Base):
    __tablename__ = "role_permissions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    role_name = Column(String(100), nullable=False)

    permission_id = Column(
        UUID(as_uuid=True),
        ForeignKey("user_permissions.id", ondelete="CASCADE"),
        nullable=False,
    )

    permission = relationship("UserPermission", back_populates="role_permissions")


# =========================================================
# OTP VERIFICATIONS
# =========================================================

class OTPVerification(Base):
    __tablename__ = "otp_verifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    mobile_number = Column(String(20), nullable=False)
    otp_code = Column(String(10), nullable=False)
    purpose = Column(String(100), nullable=False)
    is_verified = Column(Boolean, default=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


# =========================================================
# PASSWORD RESET TOKENS
# =========================================================

class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    reset_token = Column(Text, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_used = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="password_reset_tokens")


# =========================================================
# LOGIN HISTORY
# =========================================================

class LoginHistory(Base):
    __tablename__ = "login_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    ip_address = Column(String(100), nullable=True)
    device_info = Column(String(255), nullable=True)
    login_status = Column(String(50), nullable=True)

    logged_in_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="login_history")


# =========================================================
# BLOCKED USERS
# =========================================================

class BlockedUser(Base):
    __tablename__ = "blocked_users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    blocked_by_admin_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    blocked_reason = Column(Text, nullable=True)
    blocked_until = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", foreign_keys=[user_id], back_populates="blocked_users")
    blocked_by_admin = relationship("User", foreign_keys=[blocked_by_admin_id])


# =========================================================
# DRIVER PROFILE
# =========================================================

class DriverProfile(Base):
    __tablename__ = "driver_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    vehicle_id = Column(UUID(as_uuid=True), ForeignKey("vehicles.id"), nullable=True)

    subscription_plan = Column(SqlEnum(SubscriptionPlan), default=SubscriptionPlan.BASIC)
    commission_rate = Column(Numeric(5, 2), nullable=True)
    status = Column(SqlEnum(DriverStatus), default=DriverStatus.OFFLINE)

    rating = Column(Numeric(3, 2), default=5.0)
    total_trips = Column(Integer, default=0)

    user = relationship("User", back_populates="driver_profile")
    vehicle = relationship("Vehicle", back_populates="drivers")  # ✅ already exists
    trips = relationship("Trip", back_populates="driver")
    subscriptions = relationship("DriverSubscription", back_populates="driver", cascade="all, delete-orphan")
  
    locations = relationship("DriverLocation", back_populates="driver", cascade="all, delete-orphan")


# =========================================================
# KYC DOCUMENT
# =========================================================

class KYCDocument(Base):
    __tablename__ = "kyc_documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    doc_url = Column(String(255), nullable=False)

    user = relationship("User", back_populates="kyc_documents")


# =========================================================
# OTP LOG
# =========================================================

class OTPLog(Base):
    __tablename__ = "otp_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=True)

    phone = Column(String(20), nullable=False, index=True)
    otp_hash = Column(String(255), nullable=False)

    purpose = Column(SqlEnum(OTPPurpose), nullable=False)

    expires_at = Column(DateTime, nullable=False)
    used_at = Column(DateTime, nullable=True)

    attempts = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="otp_logs")


# =========================================================
# DRIVER SUBSCRIPTION
# =========================================================

class DriverSubscription(Base):
    __tablename__ = "driver_subscriptions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    driver_id = Column(
        UUID(as_uuid=True),
        ForeignKey("driver_profiles.id", ondelete="CASCADE"),
        nullable=False,
    )

    plan = Column(SqlEnum(SubscriptionPlan), nullable=False)
    commission_rate = Column(Numeric(5, 2), nullable=True)

    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)

    auto_renew = Column(Boolean, default=True)
    status = Column(String(20), default="active")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    driver = relationship("DriverProfile", back_populates="subscriptions")


# =========================================================
# DRIVER LOCATION
# =========================================================

class DriverLocation(Base):
    __tablename__ = "driver_locations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    driver_id = Column(
        UUID(as_uuid=True),
        ForeignKey("driver_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    latitude = Column(Numeric(10, 7), nullable=False)
    longitude = Column(Numeric(10, 7), nullable=False)

    heading = Column(Numeric(6, 2), nullable=True)
    speed = Column(Numeric(6, 2), nullable=True)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    driver = relationship("DriverProfile", back_populates="locations")