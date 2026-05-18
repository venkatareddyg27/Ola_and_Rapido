# models/admin.py
import uuid
import enum
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB, INET
from sqlalchemy.sql import func
from app.core.database import Base
from app.core.enums import  ActionTypeEnum


class AdminLog(Base):
    __tablename__ = "admin_logs"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # User Relationships
    admin_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    target_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, index=True)

    # Action Information
    action_type = Column(SAEnum(ActionTypeEnum), nullable=False)
    target_entity_type = Column(String(30), nullable=True)
    target_entity_id = Column(UUID(as_uuid=True), nullable=True)

    # Change Tracking
    old_value = Column(JSONB, nullable=True)
    new_value = Column(JSONB, nullable=True)
    reason = Column(Text, nullable=True)

    # Request Metadata
    ip_address = Column(INET, nullable=True)
    user_agent = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime, server_default=func.now())


class SystemConfig(Base):
    __tablename__ = "system_configs"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # Config Information
    config_key = Column(String(100), nullable=False, unique=True, index=True)
    config_value = Column(JSONB, nullable=False)
    data_type = Column(String(20), default="string")
    description = Column(Text, nullable=True)

    # Audit
    updated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

