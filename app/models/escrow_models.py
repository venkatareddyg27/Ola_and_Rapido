# =========================================================
# app/models/escrow_models.py
# =========================================================

from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    BigInteger,
    Text,
    Numeric,
)

from sqlalchemy.dialects.postgresql import JSONB

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


# =========================================================
# ESCROW HOLDS
# =========================================================

class EscrowHold(Base):
    __tablename__ = "escrow_holds"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        index=True
    )

    user_id = Column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    booking_reference_type = Column(
        String(50),
        nullable=False
    )

    booking_reference_id = Column(
        BigInteger,
        nullable=False
    )

    hold_amount = Column(
        Numeric(12, 2),
        nullable=False
    )

    released_amount = Column(
        Numeric(12, 2),
        default=0
    )

    remaining_amount = Column(
        Numeric(12, 2),
        nullable=False
    )

    escrow_status = Column(
        String(50),
        default="HELD"
    )

    remarks = Column(
        Text,
        nullable=True
    )

    held_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    released_at = Column(
        DateTime(timezone=True),
        nullable=True
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

    transactions = relationship(
        "EscrowTransaction",
        back_populates="escrow_hold",
        cascade="all, delete-orphan"
    )

    damage_claims = relationship(
        "DamageClaim",
        back_populates="escrow_hold",
        cascade="all, delete-orphan"
    )

    refunds = relationship(
        "EscrowRefund",
        back_populates="escrow_hold",
        cascade="all, delete-orphan"
    )


# =========================================================
# ESCROW TRANSACTIONS
# =========================================================

class EscrowTransaction(Base):
    __tablename__ = "escrow_transactions"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    escrow_hold_id = Column(
        BigInteger,
        ForeignKey("escrow_holds.id", ondelete="CASCADE"),
        nullable=False
    )

    transaction_type = Column(
        String(50),
        nullable=False
    )

    amount = Column(
        Numeric(12, 2),
        nullable=False
    )

    transaction_status = Column(
        String(50),
        default="SUCCESS"
    )

    remarks = Column(
        Text,
        nullable=True
    )

    processed_by = Column(
        BigInteger,
        ForeignKey("users.id"),
        nullable=True
    )

    processed_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # =====================================================
    # RELATIONSHIP
    # =====================================================

    escrow_hold = relationship(
        "EscrowHold",
        back_populates="transactions"
    )


# =========================================================
# DAMAGE CLAIMS
# =========================================================

class DamageClaim(Base):
    __tablename__ = "damage_claims"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        index=True
    )

    escrow_hold_id = Column(
        BigInteger,
        ForeignKey("escrow_holds.id", ondelete="CASCADE"),
        nullable=False
    )

    raised_by_user_id = Column(
        BigInteger,
        ForeignKey("users.id"),
        nullable=False
    )

    against_user_id = Column(
        BigInteger,
        ForeignKey("users.id"),
        nullable=False
    )

    claim_amount = Column(
        Numeric(12, 2),
        nullable=False
    )

    approved_amount = Column(
        Numeric(12, 2),
        nullable=True
    )

    damage_title = Column(
        String(255),
        nullable=False
    )

    damage_description = Column(
        Text,
        nullable=False
    )

    damage_status = Column(
        String(50),
        default="PENDING"
    )

    admin_notes = Column(
        Text,
        nullable=True
    )

    resolved_at = Column(
        DateTime(timezone=True),
        nullable=True
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

    escrow_hold = relationship(
        "EscrowHold",
        back_populates="damage_claims"
    )

    evidence_files = relationship(
        "ClaimEvidence",
        back_populates="damage_claim",
        cascade="all, delete-orphan"
    )


# =========================================================
# CLAIM EVIDENCE
# =========================================================

class ClaimEvidence(Base):
    __tablename__ = "claim_evidence"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    damage_claim_id = Column(
        BigInteger,
        ForeignKey("damage_claims.id", ondelete="CASCADE"),
        nullable=False
    )

    file_type = Column(
        String(50),
        nullable=False
    )

    file_url = Column(
        Text,
        nullable=False
    )

    uploaded_by = Column(
        BigInteger,
        ForeignKey("users.id"),
        nullable=True
    )

    upload_notes = Column(
        Text,
        nullable=True
    )

    uploaded_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # =====================================================
    # RELATIONSHIP
    # =====================================================

    damage_claim = relationship(
        "DamageClaim",
        back_populates="evidence_files"
    )


# =========================================================
# ESCROW REFUNDS
# =========================================================

class EscrowRefund(Base):
    __tablename__ = "escrow_refunds"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    escrow_hold_id = Column(
        BigInteger,
        ForeignKey("escrow_holds.id", ondelete="CASCADE"),
        nullable=False
    )

    refund_amount = Column(
        Numeric(12, 2),
        nullable=False
    )

    refund_reason = Column(
        Text,
        nullable=True
    )

    refund_status = Column(
        String(50),
        default="PENDING"
    )

    refunded_to_user_id = Column(
        BigInteger,
        ForeignKey("users.id"),
        nullable=False
    )

    processed_by_admin_id = Column(
        BigInteger,
        ForeignKey("users.id"),
        nullable=True
    )

    processed_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # =====================================================
    # RELATIONSHIP
    # =====================================================

    escrow_hold = relationship(
        "EscrowHold",
        back_populates="refunds"
    )