# payments.py

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

from models.base import Base
from core.enums import (
    PaymentMethod,
    PaymentStatus,
    WalletTransactionType,
    PayoutMethod,
    PayoutStatus
)


class Payment(Base):
    __tablename__ = "payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id")
    )

    trip_id = Column(
        UUID(as_uuid=True),
        ForeignKey("trips.id")
    )

    rental_id = Column(
        UUID(as_uuid=True),
        ForeignKey("rentals.id")
    )

    amount = Column(Numeric(10, 2))

    method = Column(Enum(PaymentMethod))

    status = Column(
        Enum(PaymentStatus),
        default=PaymentStatus.PENDING
    )
    gateway_reference = Column(String(255))
    gst_amount = Column(Numeric(10, 2))
    invoice_url = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

    # RELATIONSHIPS

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


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        unique=True
    )

    balance = Column(Numeric(10, 2), default=0.0)
    currency = Column(String(10), default="INR")
    # RELATIONSHIPS

    user = relationship(
        "User",
        back_populates="wallet"
    )

    transactions = relationship(
        "WalletTransaction",
        back_populates="wallet"
    )
   # Relationships 
    transactions = relationship(
    "WalletTransaction",
    back_populates="wallet",
    cascade="all, delete-orphan")
    
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

