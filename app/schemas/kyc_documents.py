from datetime import datetime
from typing import Optional, Dict, Any

from pydantic import BaseModel, ConfigDict

from app.core.enums import (
    DocumentType,
    VerificationStatus,
    AadhaarEKYCStatus,
    BankVerificationStatus,
    BankAccountType,
)


# =========================================================
# KYC DOCUMENT SCHEMAS
# =========================================================

class KYCDocumentBase(BaseModel):
    document_type: DocumentType
    document_number: Optional[str] = None

    front_image_url: Optional[str] = None
    back_image_url: Optional[str] = None


class KYCDocumentCreate(KYCDocumentBase):
    user_id: int


class KYCDocumentUpdate(BaseModel):
    verification_status: Optional[VerificationStatus] = None
    rejection_reason: Optional[str] = None


class KYCDocumentResponse(KYCDocumentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int

    verification_status: VerificationStatus
    rejection_reason: Optional[str] = None

    metadata_json: Optional[Dict[str, Any]] = None

    uploaded_at: datetime
    verified_at: Optional[datetime] = None

    created_at: datetime
    updated_at: datetime


# =========================================================
# AADHAAR EKYC SCHEMAS
# =========================================================

class AadhaarEKYCBase(BaseModel):
    aadhaar_last4: Optional[str] = None


class AadhaarEKYCCreate(AadhaarEKYCBase):
    user_id: int
    reference_id: str


class AadhaarEKYCUpdate(BaseModel):
    otp_verified: Optional[bool] = None
    ekyc_status: Optional[AadhaarEKYCStatus] = None


class AadhaarEKYCResponse(AadhaarEKYCBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int

    reference_id: str

    mobile_linked: bool
    otp_verified: bool

    ekyc_status: AadhaarEKYCStatus

    response_payload: Optional[Dict[str, Any]] = None

    started_at: datetime
    completed_at: Optional[datetime] = None

    created_at: datetime


# =========================================================
# PAN VERIFICATION SCHEMAS
# =========================================================

class PANVerificationBase(BaseModel):
    pan_number: str


class PANVerificationCreate(PANVerificationBase):
    user_id: int


class PANVerificationUpdate(BaseModel):
    verification_status: Optional[VerificationStatus] = None
    verified_name_match: Optional[bool] = None


class PANVerificationResponse(PANVerificationBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int

    full_name: Optional[str] = None
    date_of_birth: Optional[str] = None

    verification_status: VerificationStatus

    verified_name_match: bool

    api_reference_id: Optional[str] = None

    verification_response: Optional[Dict[str, Any]] = None

    verified_at: Optional[datetime] = None

    created_at: datetime


# =========================================================
# FACE VERIFICATION SCHEMAS
# =========================================================

class FaceVerificationBase(BaseModel):
    selfie_image_url: Optional[str] = None
    document_face_image_url: Optional[str] = None


class FaceVerificationCreate(FaceVerificationBase):
    user_id: int


class FaceVerificationUpdate(BaseModel):
    verification_status: Optional[VerificationStatus] = None
    is_face_match: Optional[bool] = None


class FaceVerificationResponse(FaceVerificationBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int

    face_match_percentage: Optional[str] = None

    is_face_match: bool

    verification_status: VerificationStatus

    provider_response: Optional[Dict[str, Any]] = None

    verified_at: Optional[datetime] = None

    created_at: datetime


# =========================================================
# SELFIE LIVENESS CHECK SCHEMAS
# =========================================================

class SelfieLivenessBase(BaseModel):
    selfie_video_url: Optional[str] = None
    selfie_image_url: Optional[str] = None


class SelfieLivenessCreate(SelfieLivenessBase):
    user_id: int


class SelfieLivenessUpdate(BaseModel):
    verification_status: Optional[VerificationStatus] = None
    is_live_person: Optional[bool] = None


class SelfieLivenessResponse(SelfieLivenessBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int

    liveness_score: Optional[str] = None

    is_live_person: bool

    verification_status: VerificationStatus

    provider_response: Optional[Dict[str, Any]] = None

    checked_at: Optional[datetime] = None

    created_at: datetime


# =========================================================
# ADDRESS VERIFICATION SCHEMAS
# =========================================================

class AddressVerificationBase(BaseModel):
    address_line_1: Optional[str] = None
    address_line_2: Optional[str] = None

    city: Optional[str] = None
    state: Optional[str] = None

    postal_code: Optional[str] = None
    country: Optional[str] = None

    proof_document_url: Optional[str] = None


class AddressVerificationCreate(AddressVerificationBase):
    user_id: int


class AddressVerificationUpdate(BaseModel):
    verification_status: Optional[VerificationStatus] = None
    verifier_notes: Optional[str] = None


class AddressVerificationResponse(AddressVerificationBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int

    verification_status: VerificationStatus

    verifier_notes: Optional[str] = None

    verified_at: Optional[datetime] = None

    created_at: datetime


# =========================================================
# BANK ACCOUNT VERIFICATION SCHEMAS
# =========================================================

class BankAccountVerificationBase(BaseModel):
    account_holder_name: Optional[str] = None

    bank_name: Optional[str] = None

    account_number: str

    ifsc_code: str

    account_type: Optional[BankAccountType] = None


class BankAccountVerificationCreate(
    BankAccountVerificationBase
):
    user_id: int


class BankAccountVerificationUpdate(BaseModel):
    penny_drop_status: Optional[
        BankVerificationStatus
    ] = None

    is_account_verified: Optional[bool] = None


class BankAccountVerificationResponse(
    BankAccountVerificationBase
):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int

    penny_drop_status: BankVerificationStatus

    is_account_verified: bool

    verification_reference: Optional[str] = None

    verification_response: Optional[
        Dict[str, Any]
    ] = None

    verified_at: Optional[datetime] = None

    created_at: datetime