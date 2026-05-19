# =========================================================
# app/models/user_models.py
# =========================================================

from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    BigInteger,
    Text,
)

from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


# =========================================================
# USERS
# =========================================================

class User(Base):
    __tablename__ = "users"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        index=True
    )

    full_name = Column(
        String(255),
        nullable=False
    )

    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    mobile_number = Column(
        String(20),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash = Column(
        Text,
        nullable=False
    )

    role = Column(
        String(50),
        default="USER"
    )

    gender = Column(
        String(20),
        nullable=True
    )

    profile_photo_url = Column(
        Text,
        nullable=True
    )

    is_active = Column(
        Boolean,
        default=True
    )

    is_verified = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    # =====================================================
    # RELATIONSHIPS
    # =====================================================

    sessions = relationship(
        "UserSession",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    devices = relationship(
        "UserDevice",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    roles = relationship(
        "UserRole",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    password_reset_tokens = relationship(
        "PasswordResetToken",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    login_history = relationship(
        "LoginHistory",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    blocked_users = relationship(
        "BlockedUser",
        primaryjoin="User.id == BlockedUser.user_id",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    coupon_usages = relationship(
    "CouponUsage",
    back_populates="user"
    )

    referral_codes = relationship(
        "ReferralCode",
        back_populates="user"
    )

# =========================================================
# USER SESSIONS
# =========================================================

class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    user_id = Column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    access_token = Column(
        Text,
        nullable=False
    )

    refresh_token = Column(
        Text,
        nullable=False
    )

    device_info = Column(
        String(255),
        nullable=True
    )

    ip_address = Column(
        String(100),
        nullable=True
    )

    expires_at = Column(
        DateTime(timezone=True)
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # =====================================================
    # RELATIONSHIP
    # =====================================================

    user = relationship(
        "User",
        back_populates="sessions"
    )


# =========================================================
# USER DEVICES
# =========================================================

class UserDevice(Base):
    __tablename__ = "user_devices"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    user_id = Column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    device_id = Column(
        String(255),
        nullable=False
    )

    device_type = Column(
        String(50),
        nullable=False
    )

    fcm_token = Column(
        Text,
        nullable=True
    )

    app_version = Column(
        String(20),
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # =====================================================
    # RELATIONSHIP
    # =====================================================

    user = relationship(
        "User",
        back_populates="devices"
    )


# =========================================================
# USER ROLES
# =========================================================

class UserRole(Base):
    __tablename__ = "user_roles"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    user_id = Column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    role_name = Column(
        String(100),
        nullable=False
    )

    assigned_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # =====================================================
    # RELATIONSHIP
    # =====================================================

    user = relationship(
        "User",
        back_populates="roles"
    )


# =========================================================
# USER PERMISSIONS
# =========================================================

class UserPermission(Base):
    __tablename__ = "user_permissions"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    permission_name = Column(
        String(100),
        unique=True,
        nullable=False
    )

    description = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # =====================================================
    # RELATIONSHIP
    # =====================================================

    role_permissions = relationship(
        "RolePermission",
        back_populates="permission",
        cascade="all, delete-orphan"
    )


# =========================================================
# ROLE PERMISSIONS
# =========================================================

class RolePermission(Base):
    __tablename__ = "role_permissions"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    role_name = Column(
        String(100),
        nullable=False
    )

    permission_id = Column(
        BigInteger,
        ForeignKey("user_permissions.id", ondelete="CASCADE"),
        nullable=False
    )

    # =====================================================
    # RELATIONSHIP
    # =====================================================

    permission = relationship(
        "UserPermission",
        back_populates="role_permissions"
    )


# =========================================================
# OTP VERIFICATIONS
# =========================================================

class OTPVerification(Base):
    __tablename__ = "otp_verifications"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    mobile_number = Column(
        String(20),
        nullable=False
    )

    otp_code = Column(
        String(10),
        nullable=False
    )

    purpose = Column(
        String(100),
        nullable=False
    )

    is_verified = Column(
        Boolean,
        default=False
    )

    expires_at = Column(
        DateTime(timezone=True),
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


# =========================================================
# PASSWORD RESET TOKENS
# =========================================================

class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    user_id = Column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    reset_token = Column(
        Text,
        nullable=False
    )

    expires_at = Column(
        DateTime(timezone=True),
        nullable=False
    )

    is_used = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # =====================================================
    # RELATIONSHIP
    # =====================================================

    user = relationship(
        "User",
        back_populates="password_reset_tokens"
    )


# =========================================================
# LOGIN HISTORY
# =========================================================

class LoginHistory(Base):
    __tablename__ = "login_history"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    user_id = Column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    ip_address = Column(
        String(100)
    )

    device_info = Column(
        String(255)
    )

    login_status = Column(
        String(50)
    )

    logged_in_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # =====================================================
    # RELATIONSHIP
    # =====================================================

    user = relationship(
        "User",
        back_populates="login_history"
    )


# =========================================================
# BLOCKED USERS
# =========================================================

class BlockedUser(Base):
    __tablename__ = "blocked_users"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    user_id = Column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    blocked_reason = Column(
        Text
    )

    blocked_by_admin_id = Column(
        BigInteger,
        ForeignKey("users.id")
    )

    blocked_until = Column(
        DateTime(timezone=True),
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # =====================================================
    # RELATIONSHIPS
    # =====================================================

    user = relationship(
        "User",
        foreign_keys=[user_id],
        back_populates="blocked_users"
    )

    blocked_by_admin = relationship(
        "User",
        foreign_keys=[blocked_by_admin_id]
    )