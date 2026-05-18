import uuid
from sqlalchemy import Column, String, Text, ForeignKey, Numeric, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.core.database import Base


class Dispute(Base):
    __tablename__ = "disputes"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # Reference Information
    reference_type = Column(String, nullable=False, index=True)
    reference_id = Column(UUID(as_uuid=True), nullable=False, index=True)

    # User Relationships
    raised_by_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    against_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    assigned_to_admin_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    # Dispute Information
    dispute_type = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)

    # Financial Information
    requested_amount = Column(Numeric(12, 2), nullable=True)
    resolution_amount_adjusted = Column(Numeric(12, 2), nullable=True)

    # Evidence Storage
    evidence_photos = Column(JSONB, default=list)
    evidence_videos = Column(JSONB, default=list)
    evidence_gps_trail = Column(JSONB, nullable=True)

    # Workflow Management
    priority = Column(String, default="medium", index=True)
    status = Column(String, default="open", index=True)
    resolution = Column(Text, nullable=True)
    escalation_count = Column(Integer, default=0)

    # SLA & R