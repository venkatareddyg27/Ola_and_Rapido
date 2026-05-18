
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel


from typing import Optional

from pydantic import BaseModel


class EscrowHoldBase(BaseModel):
    rental_id: int

    renter_user_id: int
    owner_user_id: int

    payment_id: int

    hold_reference: str

    total_amount: Decimal
    rental_amount: Decimal
    security_deposit_amount: Decimal

    gateway_name: Optional[str] = None
    gateway_hold_id: Optional[str] = None

    remarks: Optional[str] = None


class EscrowHoldCreate(EscrowHoldBase):
    pass


class EscrowHoldUpdate(BaseModel):
    status: Optional[str] = None

    deducted_amount: Optional[Decimal] = None
    refunded_amount: Optional[Decimal] = None

    released_at: Optional[datetime] = None

    remarks: Optional[str] = None


class EscrowHoldResponse(EscrowHoldBase):
    id: int

    deducted_amount: Decimal
    refunded_amount: Decimal

    status: str

    hold_created_at: datetime
    release_due_at: Optional[datetime]
    released_at: Optional[datetime]

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# =========================================================
# ESCROW TRANSACTION SCHEMAS
# =========================================================

class EscrowTransactionBase(BaseModel):
    escrow_hold_id: int

    transaction_type: str

    amount: Decimal

    transaction_reference: str

    description: Optional[str] = None


class EscrowTransactionCreate(EscrowTransactionBase):
    pass


class EscrowTransactionResponse(EscrowTransactionBase):
    id: int

    created_at: datetime

    class Config:
        from_attributes = True


# =========================================================
# DAMAGE CLAIM SCHEMAS
# =========================================================

class DamageClaimBase(BaseModel):
    escrow_hold_id: int

    rental_id: int

    owner_user_id: int
    renter_user_id: int

    claim_reference: str

    claimed_amount: Decimal

    reason: Optional[str] = None

    evidence_image_url: Optional[str] = None


class DamageClaimCreate(DamageClaimBase):
    pass


class DamageClaimUpdate(BaseModel):
    approved_amount: Optional[Decimal] = None

    admin_remarks: Optional[str] = None

    is_resolved: Optional[bool] = None

    resolved_at: Optional[datetime] = None


class DamageClaimResponse(DamageClaimBase):
    id: int

    approved_amount: Decimal

    admin_remarks: Optional[str]

    is_resolved: bool

    resolved_at: Optional[datetime]

    created_at: datetime

    class Config:
        from_attributes = True