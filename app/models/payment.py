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
from app.core.enums import (PaymentStatus, TransactionStatus, WalletTransactionType, RefundStatus)



# =========================================================
# PAYMENTS TABLE
# =========================================================

class Payment(Base):
    __tablename__ = "payments"

    id = Column(BigInteger, primary_key=True, index=True)

    ride_id = Column(BigInteger, nullable=True)
    
    rental_id = Column(BigInteger, nullable=True)

    payer_user_id = Column(BigInteger,ForeignKey("users.id"))
    
    payee_user_id = Column(BigInteger,ForeignKey("users.id"))
    
    total_amount = Column(Numeric(10, 2),nullable=False)
    
    tax_amount = Column(Numeric(10, 2),default=0)
    
    platform_fee = Column(Numeric(10, 2),default=0)
    
    final_amount = Column(Numeric(10, 2),nullable=False)
    
    payment_method = Column(String(50))
    
    status = Column(SqlEnum(PaymentStatus),default=PaymentStatus.PENDING)
    
    description = Column(Text)
    
    paid_at = Column(DateTime,nullable=True)
    
    created_at = Column(DateTime,default=datetime.utcnow)
    
    updated_at = Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
    
    transactions = relationship("PaymentTransaction",back_populates="payment",cascade="all, delete")

    invoice = relationship("Invoice",back_populates="payment",uselist=False)

    refunds = relationship("Refund",back_populates="payment",cascade="all, delete")


# =========================================================
# PAYMENT TRANSACTIONS TABLE
# =========================================================

class PaymentTransaction(Base):
    __tablename__ = "payment_transactions"

    id = Column(BigInteger, primary_key=True, index=True)

    payment_id = Column(BigInteger,ForeignKey("payments.id", ondelete="CASCADE"))

    transaction_reference = Column(String(255),unique=True,nullable=False)

    gateway_name = Column(String(100))

    gateway_transaction_id = Column(String(255))

    amount = Column(Numeric(10, 2),nullable=False)

    currency = Column(String(10),default="INR")

    status = Column(SqlEnum(TransactionStatus),default=TransactionStatus.INITIATED)

    response_message = Column(Text)

    gateway_response = Column(Text)

    is_webhook_verified = Column(Boolean,default=False)

    created_at = Column(DateTime,default=datetime.utcnow)

    payment = relationship("Payment",back_populates="transactions")


# =========================================================
# WALLETS TABLE
# =========================================================

class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(BigInteger, primary_key=True, index=True)

    user_id = Column(BigInteger,ForeignKey("users.id", ondelete="CASCADE"),unique=True)

    balance = Column(Numeric(10, 2),default=0)

    currency = Column(String(10),default="INR")

    is_active = Column(Boolean,default=True)

    created_at = Column(DateTime,default=datetime.utcnow)

    updated_at = Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)

    transactions = relationship("WalletTransaction",back_populates="wallet",cascade="all, delete")


# =========================================================
# WALLET TRANSACTIONS TABLE
# =========================================================

class WalletTransaction(Base):
    __tablename__ = "wallet_transactions"

    id = Column(BigInteger, primary_key=True, index=True)

    wallet_id = Column(BigInteger,ForeignKey("wallets.id", ondelete="CASCADE"))

    payment_id = Column(BigInteger,ForeignKey("payments.id"),nullable=True)

    transaction_type = Column(SqlEnum(WalletTransactionType))

    amount = Column(Numeric(10, 2),nullable=False)

    opening_balance = Column(Numeric(10, 2),nullable=False)

    closing_balance = Column(Numeric(10, 2),nullable=False)

    remarks = Column(Text)

    created_at = Column(DateTime,default=datetime.utcnow)

    wallet = relationship("Wallet",back_populates="transactions")


# =========================================================
# INVOICES TABLE
# =========================================================

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(BigInteger, primary_key=True, index=True)

    payment_id = Column(BigInteger,ForeignKey("payments.id", ondelete="CASCADE"),unique=True)

    invoice_number = Column(String(100),unique=True,nullable=False)

    gst_number = Column(String(50))

    subtotal = Column(Numeric(10, 2),nullable=False)

    tax_amount = Column(Numeric(10, 2),default=0)

    total_amount = Column(Numeric(10, 2),nullable=False)

    invoice_pdf_url = Column(Text)

    issued_at = Column(DateTime,default=datetime.utcnow)

    payment = relationship("Payment",back_populates="invoice")


# =========================================================
# REFUNDS TABLE
# =========================================================

class Refund(Base):
    __tablename__ = "refunds"

    id = Column(BigInteger, primary_key=True, index=True)

    payment_id = Column(BigInteger,ForeignKey("payments.id", ondelete="CASCADE"))

    refund_reference = Column(String(255),unique=True,nullable=False)

    amount = Column(Numeric(10, 2),nullable=False)

    reason = Column(Text)

    status = Column(SqlEnum(RefundStatus),default=RefundStatus.PENDING)

    processed_at = Column(DateTime,nullable=True)

    created_at = Column(DateTime,default=datetime.utcnow)

    payment = relationship("Payment",back_populates="refunds")