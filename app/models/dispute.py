from sqlalchemy import (
    Column,
    String,
    Text,
    ForeignKey,
    Numeric,
    Integer,
    BigInteger
)

from sqlalchemy.dialects.postgresql import JSONB
from app.core.database import Base


class Dispute(Base):
    __tablename__ = "disputes"

    id = Column(
    BigInteger,
    primary_key=True,
    autoincrement=True,
    index=True)

    reference_type = Column(String, nullable=False, index=True)

    reference_id = Column(
        BigInteger,
        nullable=False,
        index=True
    )

    raised_by_user_id = Column(
        BigInteger,
        ForeignKey("users.id"),
        nullable=False
    )

    against_user_id = Column(
        BigInteger,
        ForeignKey("users.id"),
        nullable=False
    )

    assigned_to_admin_id = Column(
        BigInteger,
        ForeignKey("users.id"),
        nullable=True
    )

    dispute_type = Column(String, nullable=False)

    title = Column(String, nullable=False)

    description = Column(Text, nullable=False)

    requested_amount = Column(Numeric(12, 2), nullable=True)

    resolution_amount_adjusted = Column(
        Numeric(12, 2),
        nullable=True
    )

    evidence_photos = Column(JSONB, default=list)

    evidence_videos = Column(JSONB, default=list)

    evidence_gps_trail = Column(JSONB, nullable=True)

    priority = Column(String, default="medium", index=True)

    status = Column(String, default="open", index=True)

    resolution = Column(Text, nullable=True)

    escalation_count = Column(Integer, default=0)