print("KYC MODELS IMPORTED SUCCESSFULLY")

from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    Date,
    DateTime,
    Enum as SqlEnum,
    ForeignKey,
    Numeric,
    String,
    Text,
)

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from app.core.database import Base

from app.core.enums import (
    AadhaarEkycStatus,
    DocumentType,
    VerificationStatus,
)


# =========================================================
# KYC DOCUMENT MODEL
# =========================================================

class KycDocument(Base):
    __tablename__ = "kyc_documents"

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
        index=True
    )

    document_type = Column(
        SqlEnum(DocumentType),
        nullable=False
    )

    document_url = Column(
        Text,
        nullable=False
    )

    document_hash = Column(
        String(100),
        nullable=True
    )

    ocr_extracted_data = Column(
        JSONB,
        nullable=True
    )

    ocr_confidence_score = Column(
        Numeric(5, 2),
        nullable=True
    )

    verification_status = Column(
        SqlEnum(VerificationStatus),
        default=VerificationStatus.pending,
        nullable=False
    )

    rejection_reason = Column(
        Text,
        nullable=True
    )

    verified_by_admin_id = Column(
        BigInteger,
        ForeignKey("users.id"),
        nullable=True
    )

    verified_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    expires_at = Column(
        Date,
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )


# =========================================================
# AADHAAR EKYC SESSION MODEL
# =========================================================

class AadhaarEkycSession(Base):
    __tablename__ = "aadhaar_ekyc_sessions"

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
        index=True
    )

    session_id = Column(
        String(255),
        unique=True,
        nullable=False
    )

    request_id = Column(
        String(255),
        nullable=True
    )

    otp_transaction_id = Column(
        String(255),
        nullable=True
    )

    aadhaar_last_4 = Column(
        String(4),
        nullable=True
    )

    aadhaar_tokenized_id = Column(
        String(100),
        nullable=True
    )

    uidai_response_encrypted = Column(
        Text,
        nullable=True
    )

    uidai_xml_encrypted = Column(
        Text,
        nullable=True
    )

    verified_name = Column(
        String(255),
        nullable=True
    )

    verified_dob = Column(
        Date,
        nullable=True
    )

    verified_gender = Column(
        String(10),
        nullable=True
    )

    verified_address = Column(
        Text,
        nullable=True
    )

    verified_photo_hash = Column(
        String(100),
        nullable=True
    )

    liveness_selfie_url = Column(
        Text,
        nullable=True
    )

    liveness_confidence = Column(
        Numeric(5, 2),
        nullable=True
    )

    liveness_passed = Column(
        Boolean,
        default=False
    )

    status = Column(
        SqlEnum(AadhaarEkycStatus),
        default=AadhaarEkycStatus.otp_sent,
        nullable=False
    )

    error_reason = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    expires_at = Column(
        DateTime(timezone=True),
        nullable=False
    )

    completed_at = Column(
        DateTime(timezone=True),
        nullable=True
    )