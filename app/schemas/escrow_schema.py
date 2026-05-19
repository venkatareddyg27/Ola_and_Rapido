
from pydantic import (
    BaseModel,
    ConfigDict
)

from typing import Optional
from decimal import Decimal
from datetime import datetime

from app.core.enums import (
    EscrowStatusEnum,
    EscrowTransactionTypeEnum,
    EscrowTransactionStatusEnum,
    DamageClaimStatusEnum,
    DamageSeverityEnum,
    ClaimEvidenceTypeEnum,
    EscrowRefundStatusEnum,
    BookingReferenceTypeEnum,
    ClaimResolutionTypeEnum,
)


# =========================================================
# ESCROW HOLD SCHEMAS
# =========================================================

class EscrowHoldCreate(BaseModel):
    user_id: int
    booking_reference_type: BookingReferenceTypeEnum
    booking_reference_id: int
    hold_amount: Decimal
    remarks: Optional[str] = None


class EscrowHoldResponse(BaseModel):
    id: int
    user_id: int
    booking_reference_type: BookingReferenceTypeEnum
    booking_reference_id: int
    hold_amount: Decimal
    released_amount: Decimal
    remaining_amount: Decimal
    escrow_status: EscrowStatusEnum
    remarks: Optional[str]
    held_at: datetime
    released_at: Optional[datetime]
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# ESCROW TRANSACTION SCHEMAS
# =========================================================

class EscrowTransactionCreate(BaseModel):
    escrow_hold_id: int
    transaction_type: EscrowTransactionTypeEnum
    amount: Decimal
    remarks: Optional[str] = None
    processed_by: Optional[int] = None


class EscrowTransactionResponse(BaseModel):
    id: int
    escrow_hold_id: int
    transaction_type: EscrowTransactionTypeEnum
    amount: Decimal
    transaction_status: EscrowTransactionStatusEnum
    remarks: Optional[str]
    processed_by: Optional[int]
    processed_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# DAMAGE CLAIM SCHEMAS
# =========================================================

class DamageClaimCreate(BaseModel):
    escrow_hold_id: int
    raised_by_user_id: int
    against_user_id: int
    claim_amount: Decimal
    damage_title: str
    damage_description: str


class DamageClaimUpdate(BaseModel):
    approved_amount: Optional[Decimal] = None
    damage_status: Optional[DamageClaimStatusEnum] = None
    admin_notes: Optional[str] = None


class DamageClaimResponse(BaseModel):
    id: int
    escrow_hold_id: int
    raised_by_user_id: int
    against_user_id: int
    claim_amount: Decimal
    approved_amount: Optional[Decimal]
    damage_title: str
    damage_description: str
    damage_status: DamageClaimStatusEnum
    admin_notes: Optional[str]
    resolved_at: Optional[datetime]
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# CLAIM EVIDENCE SCHEMAS
# =========================================================

class ClaimEvidenceCreate(BaseModel):
    damage_claim_id: int
    file_type: ClaimEvidenceTypeEnum
    file_url: str
    uploaded_by: Optional[int] = None
    upload_notes: Optional[str] = None


class ClaimEvidenceResponse(BaseModel):
    id: int
    damage_claim_id: int
    file_type: ClaimEvidenceTypeEnum
    file_url: str
    uploaded_by: Optional[int]
    upload_notes: Optional[str]
    uploaded_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# ESCROW REFUND SCHEMAS
# =========================================================

class EscrowRefundCreate(BaseModel):
    escrow_hold_id: int
    refund_amount: Decimal
    refund_reason: Optional[str] = None
    refunded_to_user_id: int


class EscrowRefundUpdate(BaseModel):
    refund_status: EscrowRefundStatusEnum
    processed_by_admin_id: Optional[int] = None


class EscrowRefundResponse(BaseModel):
    id: int
    escrow_hold_id: int
    refund_amount: Decimal
    refund_reason: Optional[str]
    refund_status: EscrowRefundStatusEnum
    refunded_to_user_id: int
    processed_by_admin_id: Optional[int]
    processed_at: Optional[datetime]
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# DAMAGE CLAIM RESOLUTION SCHEMA
# =========================================================

class DamageClaimResolution(BaseModel):
    claim_id: int
    resolution_type: ClaimResolutionTypeEnum
    approved_amount: Decimal
    admin_notes: Optional[str] = None


# =========================================================
# ESCROW SUMMARY RESPONSE
# =========================================================

class EscrowSummaryResponse(BaseModel):
    total_held_amount: Decimal
    total_released_amount: Decimal
    total_refunded_amount: Decimal
    total_damage_claims: int