
from pydantic import (
    BaseModel,
    ConfigDict
)

from typing import Optional, Dict, Any
from decimal import Decimal
from datetime import datetime

from app.core.enums import (
    PaymentStatusEnum,
    PaymentMethodTypeEnum,
    WalletTransactionTypeEnum,
    WalletRechargeStatusEnum,
    PaymentTransactionStatusEnum,
    RefundStatusEnum,
    InvoiceStatusEnum,
    SettlementStatusEnum,
    PaymentGatewayEnum,
    CurrencyEnum,
    PaymentReferenceTypeEnum,
    GatewayLogStatusEnum,
)


# =========================================================
# WALLET SCHEMAS
# =========================================================

class WalletCreate(BaseModel):
    user_id: int
    currency: CurrencyEnum = CurrencyEnum.INR


class WalletResponse(BaseModel):
    id: int
    user_id: int
    balance: Decimal
    currency: CurrencyEnum
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# WALLET TRANSACTION SCHEMAS
# =========================================================

class WalletTransactionCreate(BaseModel):
    wallet_id: int
    transaction_type: WalletTransactionTypeEnum
    amount: Decimal
    opening_balance: Optional[Decimal] = None
    closing_balance: Optional[Decimal] = None
    reference_type: Optional[PaymentReferenceTypeEnum] = None
    reference_id: Optional[int] = None
    description: Optional[str] = None


class WalletTransactionResponse(BaseModel):
    id: int
    wallet_id: int
    transaction_type: WalletTransactionTypeEnum
    amount: Decimal
    opening_balance: Optional[Decimal]
    closing_balance: Optional[Decimal]
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# WALLET RECHARGE SCHEMAS
# =========================================================

class WalletRechargeCreate(BaseModel):
    wallet_id: int
    recharge_amount: Decimal


class WalletRechargeResponse(BaseModel):
    id: int
    wallet_id: int
    payment_id: Optional[int]
    recharge_amount: Decimal
    recharge_status: WalletRechargeStatusEnum
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# PAYMENT METHOD SCHEMAS
# =========================================================

class PaymentMethodCreate(BaseModel):
    user_id: int
    method_type: PaymentMethodTypeEnum
    provider_name: Optional[str] = None
    masked_account_number: Optional[str] = None
    upi_id: Optional[str] = None
    is_default: bool = False


class PaymentMethodResponse(BaseModel):
    id: int
    user_id: int
    method_type: PaymentMethodTypeEnum
    provider_name: Optional[str]
    masked_account_number: Optional[str]
    upi_id: Optional[str]
    is_default: bool
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# PAYMENT SCHEMAS
# =========================================================

class PaymentCreate(BaseModel):
    user_id: int
    payment_method_id: Optional[int] = None
    amount: Decimal
    currency: CurrencyEnum = CurrencyEnum.INR
    remarks: Optional[str] = None


class PaymentResponse(BaseModel):
    id: int
    user_id: int
    payment_method_id: Optional[int]
    amount: Decimal
    currency: CurrencyEnum
    payment_status: PaymentStatusEnum
    gateway_transaction_id: Optional[str]
    paid_at: Optional[datetime]
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# PAYMENT TRANSACTION SCHEMAS
# =========================================================

class PaymentTransactionCreate(BaseModel):
    payment_id: int
    transaction_status: PaymentTransactionStatusEnum
    gateway_name: Optional[PaymentGatewayEnum] = None
    gateway_response: Optional[Dict[str, Any]] = None
    transaction_reference: Optional[str] = None


class PaymentTransactionResponse(BaseModel):
    id: int
    payment_id: int
    transaction_status: PaymentTransactionStatusEnum
    gateway_name: Optional[PaymentGatewayEnum]
    transaction_reference: Optional[str]
    processed_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# REFUND SCHEMAS
# =========================================================

class RefundCreate(BaseModel):
    payment_id: int
    refund_amount: Decimal
    refund_reason: Optional[str] = None


class RefundResponse(BaseModel):
    id: int
    payment_id: int
    refund_amount: Decimal
    refund_reason: Optional[str]
    refund_status: RefundStatusEnum
    gateway_refund_id: Optional[str]
    processed_at: Optional[datetime]
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# INVOICE SCHEMAS
# =========================================================

class InvoiceCreate(BaseModel):
    payment_id: int
    invoice_number: str
    subtotal: Decimal
    tax_amount: Decimal
    total_amount: Decimal


class InvoiceResponse(BaseModel):
    id: int
    payment_id: int
    invoice_number: str
    subtotal: Decimal
    tax_amount: Decimal
    total_amount: Decimal
    invoice_pdf_url: Optional[str]
    generated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# TAX INVOICE SCHEMAS
# =========================================================

class TaxInvoiceCreate(BaseModel):
    invoice_id: int
    gst_number: Optional[str] = None
    cgst_amount: Decimal = Decimal("0")
    sgst_amount: Decimal = Decimal("0")
    igst_amount: Decimal = Decimal("0")


class TaxInvoiceResponse(BaseModel):
    id: int
    invoice_id: int
    gst_number: Optional[str]
    cgst_amount: Decimal
    sgst_amount: Decimal
    igst_amount: Decimal
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# SETTLEMENT REPORT SCHEMAS
# =========================================================

class SettlementReportCreate(BaseModel):
    report_name: str
    total_transactions: int
    total_amount: Decimal
    report_data: Optional[Dict[str, Any]] = None
    generated_by: Optional[int] = None


class SettlementReportResponse(BaseModel):
    id: int
    report_name: str
    total_transactions: int
    total_amount: Decimal
    generated_by: Optional[int]
    generated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# GATEWAY LOG SCHEMAS
# =========================================================

class GatewayLogCreate(BaseModel):
    payment_id: int
    gateway_name: PaymentGatewayEnum
    request_payload: Optional[Dict[str, Any]] = None
    response_payload: Optional[Dict[str, Any]] = None
    http_status_code: Optional[str] = None
    is_success: bool = False


class GatewayLogResponse(BaseModel):
    id: int
    payment_id: int
    gateway_name: PaymentGatewayEnum
    http_status_code: Optional[str]
    is_success: bool
    logged_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )