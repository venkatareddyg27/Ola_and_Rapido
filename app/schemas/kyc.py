from datetime import date, datetime
from decimal import Decimal
from typing import Any, Dict, Optional
from pydantic import BaseModel, ConfigDict
from app.core.enums import (
     AadhaarEkycStatus,
    DocumentType,
    VerificationStatus,
)
# =========================================================
# KYC DOCUMENT SCHEMAS
# =========================================================

class KycDocumentCreate(BaseModel):
    user_id: int
    document_type: DocumentType
    document_url: str
    document_hash: Optional[str] = None
    expires_at: Optional[date] = None


class KycDocumentUpdate(BaseModel):
    verification_status: Optional[VerificationStatus] = None
    rejection_reason: Optional[str] = None
    verified_by_admin_id: Optional[int] = None
    verified_at: Optional[datetime] = None
    ocr_extracted_data: Optional[Dict[str, Any]] = None
    ocr_confidence_score: Optional[Decimal] = None


class KycDocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    document_type: DocumentType
    document_url: str
    document_hash: Optional[str]
    ocr_extracted_data: Optional[Dict[str, Any]]
    ocr_confidence_score: Optional[Decimal]
    verification_status: VerificationStatus
    rejection_reason: Optional[str]
    verified_by_admin_id: Optional[int]
    verified_at: Optional[datetime]
    expires_at: Optional[date]
    created_at: datetime
    updated_at: datetime


# =========================================================
# AADHAAR EKYC SESSION SCHEMAS
# =========================================================

class AadhaarEkycSessionCreate(BaseModel):
    user_id: int
    aadhaar_last_4: str


class AadhaarEkycSessionUpdate(BaseModel):
    request_id: Optional[str] = None
    otp_transaction_id: Optional[str] = None
    status: Optional[AadhaarEkycStatus] = None
    liveness_selfie_url: Optional[str] = None
    liveness_confidence: Optional[Decimal] = None
    liveness_passed: Optional[bool] = None
    error_reason: Optional[str] = None
    completed_at: Optional[datetime] = None


class AadhaarEkycSessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    session_id: str
    request_id: Optional[str]
    otp_transaction_id: Optional[str]
    aadhaar_last_4: Optional[str]
    aadhaar_tokenized_id: Optional[str]
    verified_name: Optional[str]
    verified_dob: Optional[date]
    verified_gender: Optional[str]
    verified_address: Optional[str]
    verified_photo_hash: Optional[str]
    liveness_selfie_url: Optional[str]
    liveness_confidence: Optional[Decimal]
    liveness_passed: bool
    status: AadhaarEkycStatus
    error_reason: Optional[str]
    created_at: datetime
    expires_at: datetime
    completed_at: Optional[datetime]