from datetime import datetime
from enum import Enum

from sqlalchemy import (
    Column,
    String,
    BigInteger,
    DateTime,
    ForeignKey,
    Numeric,
    Text,
    Boolean,
    Enum as SqlEnum
)

from sqlalchemy.orm import relationship

from app.core.database import Base


from app.core.enums import (EscrowStatus, EscrowTransactionType)


# =========================================================
# ESCROW HOLDS TABLE
# =========================================================

class EscrowHold(Base):
    __tablename__ = "escrow_holds"

    id = Column(BigInteger, primary_key=True, index=True)

    rental_id = Column(BigInteger,nullable=False)

    renter_user_id = Column(BigInteger,ForeignKey("users.id"),nullable=False)

    owner_user_id = Column(BigInteger,ForeignKey("users.id"),nullable=False)

    payment_id = Column(BigInteger,ForeignKey("payments.id"),nullable=False)

    hold_reference = Column(String(255),unique=True,nullable=False)

    total_amount = Column(Numeric(10, 2),nullable=False)

    rental_amount = Column(Numeric(10, 2),nullable=False)

    security_deposit_amount = Column(Numeric(10, 2),nullable=False)

    deducted_amount = Column(Numeric(10, 2),default=0)

    refunded_amount = Column(Numeric(10, 2),default=0)

    status = Column(SqlEnum(EscrowStatus),default=EscrowStatus.INITIATED)

    gateway_name = Column(String(100))

    gateway_hold_id = Column(String(255))

    hold_created_at = Column(DateTime,default=datetime.utcnow)

    release_due_at = Column(DateTime,nullable=True)
    
    released_at = Column(DateTime,nullable=True)

    remarks = Column(Text)

    created_at = Column(DateTime,default=datetime.utcnow)
    
    updated_at = Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)

    transactions = relationship("EscrowTransaction",back_populates="escrow_hold",cascade="all, delete")

    damage_claims = relationship("DamageClaim",back_populates="escrow_hold",cascade="all, delete")


# =========================================================
# ESCROW TRANSACTIONS TABLE
# =========================================================

class EscrowTransaction(Base):
    __tablename__ = "escrow_transactions"

    id = Column(BigInteger, primary_key=True, index=True)

    escrow_hold_id = Column(BigInteger,ForeignKey("escrow_holds.id", ondelete="CASCADE"),nullable=False)

    transaction_type = Column(SqlEnum(EscrowTransactionType),nullable=False)

    amount = Column(Numeric(10, 2),nullable=False)

    transaction_reference = Column(String(255),unique=True,nullable=False)

    description = Column(Text)

    created_at = Column(DateTime,default=datetime.utcnow)

    escrow_hold = relationship("EscrowHold",back_populates="transactions")


# =========================================================
# DAMAGE CLAIMS TABLE
# =========================================================

class DamageClaim(Base):
    __tablename__ = "damage_claims"

    id = Column(BigInteger, primary_key=True, index=True)

    escrow_hold_id = Column(BigInteger,ForeignKey("escrow_holds.id", ondelete="CASCADE"),nullable=False)

    rental_id = Column(BigInteger,nullable=False)

    owner_user_id = Column(BigInteger,ForeignKey("users.id"),nullable=False)

    renter_user_id = Column(BigInteger,ForeignKey("users.id"),nullable=False)

    claim_reference = Column(String(255),unique=True,nullable=False)

    claimed_amount = Column(Numeric(10, 2),nullable=False)

    approved_amount = Column(Numeric(10, 2),default=0)

    reason = Column(Text)

    evidence_image_url = Column(Text)

    admin_remarks = Column(Text)

    is_resolved = Column(Boolean,default=False)

    resolved_at = Column(DateTime,nullable=True)

    created_at = Column(DateTime,default=datetime.utcnow)

    escrow_hold = relationship("DamageClaim",back_populates="damage_claims")