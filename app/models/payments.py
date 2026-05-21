import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Numeric,
    Enum,
    String
)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base

from app.core.enums import (
    PaymentMethod,
    PaymentStatus,
    WalletTransactionType,
    PayoutMethod,
    PayoutStatus
)


# =========================================================
# PAYMENT MODEL
# =========================================================

class Payment(Base):

    __tablename__ = "payments"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    trip_id = Column(
        UUID(as_uuid=True),
        ForeignKey("trips.id"),
        nullable=True
    )

    rental_id = Column(
        UUID(as_uuid=True),
        ForeignKey("rentals.id"),
        nullable=True
    )

    amount = Column(
        Numeric(10, 2),
        nullable=False
    )

    method = Column(
        Enum(PaymentMethod),
        nullable=False
    )

    status = Column(
        Enum(PaymentStatus),
        default=PaymentStatus.PENDING
    )

    gateway_reference = Column(
        String(255),
        nullable=True
    )

    gst_amount = Column(
        Numeric(10, 2),
        nullable=True
    )

    invoice_url = Column(
        String(255),
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    # =====================================================
    # RELATIONSHIPS
    # =====================================================

    user = relationship(
        "User",
        back_populates="payments"
    )

    trip = relationship(
        "Trip",
        back_populates="payments"
    )

    rental = relationship(
        "Rental",
        back_populates="payments"
    )


# =========================================================
# WALLET MODEL
# =========================================================

class Wallet(Base):

    __tablename__ = "wallets"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    balance = Column(
        Numeric(10, 2),
        default=0.0
    )

    currency = Column(
        String(10),
        default="INR"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    # =====================================================
    # RELATIONSHIPS
    # =====================================================

    user = relationship(
        "User",
        back_populates="wallet"
    )

    transactions = relationship(
        "WalletTransaction",
        back_populates="wallet",
        cascade="all, delete-orphan"
    )


# =========================================================
# WALLET TRANSACTION MODEL
# =========================================================

class WalletTransaction(Base):

    __tablename__ = "wallet_transactions"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    wallet_id = Column(
        UUID(as_uuid=True),
        ForeignKey("wallets.id", ondelete="CASCADE"),
        nullable=False
    )

    type = Column(
        Enum(WalletTransactionType),
        nullable=False
    )

    amount = Column(
        Numeric(10, 2),
        nullable=False
    )

    reason = Column(
        String(255),
        nullable=False
    )

    reference_id = Column(
        String(255),
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # =====================================================
    # RELATIONSHIPS
    # =====================================================

    wallet = relationship(
        "Wallet",
        back_populates="transactions"
    )


# =========================================================
# DRIVER PAYOUT MODEL
# =========================================================

class DriverPayout(Base):

    __tablename__ = "driver_payouts"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    driver_id = Column(
        UUID(as_uuid=True),
        ForeignKey("driver_profiles.id", ondelete="CASCADE"),
        nullable=False
    )

    amount = Column(
        Numeric(10, 2),
        nullable=False
    )

    method = Column(
        Enum(PayoutMethod),
        nullable=False
    )

    # =====================================================
    # UPI DETAILS
    # =====================================================

    upi_id = Column(
        String(100),
        nullable=True
    )

    # =====================================================
    # BANK DETAILS
    # =====================================================

    bank_account = Column(
        String(50),
        nullable=True
    )

    bank_ifsc = Column(
        String(20),
        nullable=True
    )

    # =====================================================
    # PAYOUT STATUS
    # =====================================================

    status = Column(
        Enum(PayoutStatus),
        default=PayoutStatus.PENDING,
        nullable=False
    )

    requested_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    processed_at = Column(
        DateTime,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # =====================================================
    # RELATIONSHIPS
    # =====================================================

    driver = relationship(
        "DriverProfile",
        back_populates="payouts"
    )