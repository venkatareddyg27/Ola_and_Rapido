from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Text,
    JSON,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


# =========================================================
# KYC DOCUMENTS
# =========================================================

class KYCDocument(Base):
    __tablename__ = "kyc_documents"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    document_type = Column(String, nullable=False)
    document_number = Column(String, nullable=True)

    front_image_url = Column(String, nullable=True)
    back_image_url = Column(String, nullable=True)

    verification_status = Column(String, default="PENDING")

    rejection_reason = Column(Text, nullable=True)

    metadata_json = Column(JSON, nullable=True)

    uploaded_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    verified_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    # -----------------------------------------------------
    # RELATIONSHIPS
    # -----------------------------------------------------

    user = relationship(
        "User",
        back_populates="kyc_documents"
    )


# =========================================================
# AADHAAR EKYC SESSIONS
# =========================================================

class AadhaarEKYCSession(Base):
    __tablename__ = "aadhaar_ekyc_sessions"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    reference_id = Column(String, unique=True, nullable=False)

    aadhaar_last4 = Column(String(4), nullable=True)

    mobile_linked = Column(Boolean, default=False)

    otp_verified = Column(Boolean, default=False)

    ekyc_status = Column(String, default="INITIATED")

    response_payload = Column(JSON, nullable=True)

    started_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    completed_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # -----------------------------------------------------
    # RELATIONSHIPS
    # -----------------------------------------------------

    user = relationship(
        "User",
        back_populates="aadhaar_ekyc_sessions"
    )


# =========================================================
# PAN VERIFICATIONS
# =========================================================

class PANVerification(Base):
    __tablename__ = "pan_verifications"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    pan_number = Column(String(10), nullable=False)

    full_name = Column(String, nullable=True)

    date_of_birth = Column(String, nullable=True)

    verification_status = Column(String, default="PENDING")

    verified_name_match = Column(Boolean, default=False)

    api_reference_id = Column(String, nullable=True)

    verification_response = Column(JSON, nullable=True)

    verified_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # -----------------------------------------------------
    # RELATIONSHIPS
    # -----------------------------------------------------

    user = relationship(
        "User",
        back_populates="pan_verifications"
    )


# =========================================================
# FACE VERIFICATIONS
# =========================================================

class FaceVerification(Base):
    __tablename__ = "face_verifications"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    selfie_image_url = Column(String, nullable=True)

    document_face_image_url = Column(String, nullable=True)

    face_match_percentage = Column(String, nullable=True)

    is_face_match = Column(Boolean, default=False)

    verification_status = Column(String, default="PENDING")

    provider_response = Column(JSON, nullable=True)

    verified_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # -----------------------------------------------------
    # RELATIONSHIPS
    # -----------------------------------------------------

    user = relationship(
        "User",
        back_populates="face_verifications"
    )


# =========================================================
# SELFIE LIVENESS CHECKS
# =========================================================

class SelfieLivenessCheck(Base):
    __tablename__ = "selfie_liveness_checks"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    selfie_video_url = Column(String, nullable=True)

    selfie_image_url = Column(String, nullable=True)

    liveness_score = Column(String, nullable=True)

    is_live_person = Column(Boolean, default=False)

    verification_status = Column(String, default="PENDING")

    provider_response = Column(JSON, nullable=True)

    checked_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # -----------------------------------------------------
    # RELATIONSHIPS
    # -----------------------------------------------------

    user = relationship(
        "User",
        back_populates="selfie_liveness_checks"
    )


# =========================================================
# ADDRESS VERIFICATIONS
# =========================================================

class AddressVerification(Base):
    __tablename__ = "address_verifications"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    address_line_1 = Column(String, nullable=True)
    address_line_2 = Column(String, nullable=True)

    city = Column(String, nullable=True)
    state = Column(String, nullable=True)

    postal_code = Column(String, nullable=True)

    country = Column(String, nullable=True)

    proof_document_url = Column(String, nullable=True)

    verification_status = Column(String, default="PENDING")

    verifier_notes = Column(Text, nullable=True)

    verified_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # -----------------------------------------------------
    # RELATIONSHIPS
    # -----------------------------------------------------

    user = relationship(
        "User",
        back_populates="address_verifications"
    )


# =========================================================
# BANK ACCOUNT VERIFICATIONS
# =========================================================

class BankAccountVerification(Base):
    __tablename__ = "bank_account_verifications"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    account_holder_name = Column(String, nullable=True)

    bank_name = Column(String, nullable=True)

    account_number = Column(String, nullable=False)

    ifsc_code = Column(String, nullable=False)

    account_type = Column(String, nullable=True)

    penny_drop_status = Column(String, default="PENDING")

    is_account_verified = Column(Boolean, default=False)

    verification_reference = Column(String, nullable=True)

    verification_response = Column(JSON, nullable=True)

    verified_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # -----------------------------------------------------
    # RELATIONSHIPS
    # -----------------------------------------------------

    user = relationship(
        "User",
        back_populates="bank_account_verifications"
    )