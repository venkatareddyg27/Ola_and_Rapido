
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
# WALLETS
# =========================================================

class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        index=True
    )

    user_id = Column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )

    balance = Column(
        Numeric(12, 2),
        default=0
    )

    currency = Column(
        String(10),
        default="INR"
    )

    is_active = Column(
        Boolean,
        default=True
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
        "WalletTransaction",
        back_populates="wallet",
        cascade="all, delete-orphan"
    )

    recharges = relationship(
        "WalletRecharge",
        back_populates="wallet",
        cascade="all, delete-orphan"
    )


# =========================================================
# WALLET TRANSACTIONS
# =========================================================

class WalletTransaction(Base):
    __tablename__ = "wallet_transactions"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    wallet_id = Column(
        BigInteger,
        ForeignKey("wallets.id", ondelete="CASCADE"),
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

    opening_balance = Column(
        Numeric(12, 2),
        nullable=True
    )

    closing_balance = Column(
        Numeric(12, 2),
        nullable=True
    )

    reference_type = Column(
        String(50),
        nullable=True
    )

    reference_id = Column(
        BigInteger,
        nullable=True
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

    wallet = relationship(
        "Wallet",
        back_populates="transactions"
    )


# =========================================================
# WALLET RECHARGES
# =========================================================

class WalletRecharge(Base):
    __tablename__ = "wallet_recharges"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    wallet_id = Column(
        BigInteger,
        ForeignKey("wallets.id", ondelete="CASCADE"),
        nullable=False
    )

    payment_id = Column(
        BigInteger,
        ForeignKey("payments.id"),
        nullable=True
    )

    recharge_amount = Column(
        Numeric(12, 2),
        nullable=False
    )

    recharge_status = Column(
        String(50),
        default="PENDING"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # =====================================================
    # RELATIONSHIPS
    # =====================================================

    wallet = relationship(
        "Wallet",
        back_populates="recharges"
    )

    payment = relationship(
        "Payment",
        back_populates="wallet_recharge"
    )


# =========================================================
# PAYMENTS
# =========================================================

class Payment(Base):
    __tablename__ = "payments"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        index=True
    )

    user_id = Column(
        BigInteger,
        ForeignKey("users.id"),
        nullable=False
    )

    payment_method_id = Column(
        BigInteger,
        ForeignKey("payment_methods.id"),
        nullable=True
    )

    amount = Column(
        Numeric(12, 2),
        nullable=False
    )

    currency = Column(
        String(10),
        default="INR"
    )

    payment_status = Column(
        String(50),
        default="PENDING"
    )

    gateway_transaction_id = Column(
        String(255),
        nullable=True
    )

    gateway_response = Column(
        JSONB,
        nullable=True
    )

    remarks = Column(
        Text,
        nullable=True
    )

    paid_at = Column(
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

    transactions = relationship(
        "PaymentTransaction",
        back_populates="payment",
        cascade="all, delete-orphan"
    )

    refunds = relationship(
        "Refund",
        back_populates="payment",
        cascade="all, delete-orphan"
    )

    invoices = relationship(
        "Invoice",
        back_populates="payment",
        cascade="all, delete-orphan"
    )

    wallet_recharge = relationship(
        "WalletRecharge",
        back_populates="payment",
        uselist=False
    )

    gateway_logs = relationship(
        "GatewayLog",
        back_populates="payment",
        cascade="all, delete-orphan"
    )


# =========================================================
# PAYMENT TRANSACTIONS
# =========================================================

class PaymentTransaction(Base):
    __tablename__ = "payment_transactions"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    payment_id = Column(
        BigInteger,
        ForeignKey("payments.id", ondelete="CASCADE"),
        nullable=False
    )

    transaction_status = Column(
        String(50),
        nullable=False
    )

    gateway_name = Column(
        String(100),
        nullable=True
    )

    gateway_response = Column(
        JSONB,
        nullable=True
    )

    transaction_reference = Column(
        String(255),
        nullable=True
    )

    processed_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # =====================================================
    # RELATIONSHIP
    # =====================================================

    payment = relationship(
        "Payment",
        back_populates="transactions"
    )


# =========================================================
# PAYMENT METHODS
# =========================================================

class PaymentMethod(Base):
    __tablename__ = "payment_methods"

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

    method_type = Column(
        String(50),
        nullable=False
    )

    provider_name = Column(
        String(100),
        nullable=True
    )

    masked_account_number = Column(
        String(50),
        nullable=True
    )

    upi_id = Column(
        String(100),
        nullable=True
    )

    is_default = Column(
        Boolean,
        default=False
    )

    is_active = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # =====================================================
    # RELATIONSHIPS
    # =====================================================

    payments = relationship(
        "Payment",
        backref="payment_method"
    )


# =========================================================
# REFUNDS
# =========================================================

class Refund(Base):
    __tablename__ = "refunds"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    payment_id = Column(
        BigInteger,
        ForeignKey("payments.id", ondelete="CASCADE"),
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

    gateway_refund_id = Column(
        String(255),
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

    payment = relationship(
        "Payment",
        back_populates="refunds"
    )


# =========================================================
# INVOICES
# =========================================================

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    payment_id = Column(
        BigInteger,
        ForeignKey("payments.id", ondelete="CASCADE"),
        nullable=False
    )

    invoice_number = Column(
        String(100),
        unique=True,
        nullable=False
    )

    subtotal = Column(
        Numeric(12, 2),
        nullable=False
    )

    tax_amount = Column(
        Numeric(12, 2),
        default=0
    )

    total_amount = Column(
        Numeric(12, 2),
        nullable=False
    )

    invoice_pdf_url = Column(
        Text,
        nullable=True
    )

    generated_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # =====================================================
    # RELATIONSHIP
    # =====================================================

    payment = relationship(
        "Payment",
        back_populates="invoices"
    )

    tax_invoice = relationship(
        "TaxInvoice",
        back_populates="invoice",
        uselist=False,
        cascade="all, delete-orphan"
    )


# =========================================================
# TAX INVOICES
# =========================================================

class TaxInvoice(Base):
    __tablename__ = "tax_invoices"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    invoice_id = Column(
        BigInteger,
        ForeignKey("invoices.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )

    gst_number = Column(
        String(50),
        nullable=True
    )

    cgst_amount = Column(
        Numeric(12, 2),
        default=0
    )

    sgst_amount = Column(
        Numeric(12, 2),
        default=0
    )

    igst_amount = Column(
        Numeric(12, 2),
        default=0
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # =====================================================
    # RELATIONSHIP
    # =====================================================

    invoice = relationship(
        "Invoice",
        back_populates="tax_invoice"
    )


# =========================================================
# SETTLEMENT REPORTS
# =========================================================

class SettlementReport(Base):
    __tablename__ = "settlement_reports"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    report_name = Column(
        String(255),
        nullable=False
    )

    total_transactions = Column(
        BigInteger,
        default=0
    )

    total_amount = Column(
        Numeric(14, 2),
        default=0
    )

    report_data = Column(
        JSONB,
        nullable=True
    )

    generated_by = Column(
        BigInteger,
        ForeignKey("users.id"),
        nullable=True
    )

    generated_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


# =========================================================
# GATEWAY LOGS
# =========================================================

class GatewayLog(Base):
    __tablename__ = "gateway_logs"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    payment_id = Column(
        BigInteger,
        ForeignKey("payments.id", ondelete="CASCADE"),
        nullable=False
    )

    gateway_name = Column(
        String(100),
        nullable=False
    )

    request_payload = Column(
        JSONB,
        nullable=True
    )

    response_payload = Column(
        JSONB,
        nullable=True
    )

    http_status_code = Column(
        String(10),
        nullable=True
    )

    is_success = Column(
        Boolean,
        default=False
    )

    logged_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # =====================================================
    # RELATIONSHIP
    # =====================================================

    payment = relationship(
        "Payment",
        back_populates="gateway_logs"
    )