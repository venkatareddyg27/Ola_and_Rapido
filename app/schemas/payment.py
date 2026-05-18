from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


# =========================================================
# PAYMENT SCHEMAS
# =========================================================

class PaymentBase(BaseModel):
    ride_id: Optional[int] = None
    rental_id: Optional[int] = None

    payer_user_id: int
    payee_user_id: int

    total_amount: Decimal
    tax_amount: Decimal = 0
    platform_fee: Decimal = 0
    final_amount: Decimal

    payment_method: Optional[str] = None
    description: Optional[str] = None


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    status: Optional[str] = None
    payment_method: Optional[str] = None
    description: Optional[str] = None
    paid_at: Optional[datetime] = None


class PaymentResponse(PaymentBase):
    id: int
    status: str
    paid_at: Optional[datetime]

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# =========================================================
# PAYMENT TRANSACTION SCHEMAS
# =========================================================

class PaymentTransactionBase(BaseModel):
    payment_id: int

    transaction_reference: str

    gateway_name: Optional[str] = None
    gateway_transaction_id: Optional[str] = None

    amount: Decimal
    currency: str = "INR"

    response_message: Optional[str] = None
    gateway_response: Optional[str] = None


class PaymentTransactionCreate(PaymentTransactionBase):
    pass


class PaymentTransactionResponse(PaymentTransactionBase):
    id: int
    status: str
    is_webhook_verified: bool

    created_at: datetime

    class Config:
        from_attributes = True


