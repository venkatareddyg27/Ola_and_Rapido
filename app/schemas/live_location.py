from uuid import UUID
from decimal import Decimal
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

class DisputeBaseSchema(BaseModel):
    reference_type: str
    reference_id: UUID
    raised_by_user_id: UUID
    against_user_id: UUID
    dispute_type: str
    title: str = Field(..., max_length=255)
    description: str
    requested_amount: Optional[Decimal] = None
    evidence_photos: Optional[List[str]] = Field(default_factory=list)
    evidence_videos: Optional[List[str]] = Field(default_factory=list)
    evidence_gps_trail: Optional[Dict[str, Any]] = None

class DisputeCreateSchema(DisputeBaseSchema):
    pass

class DisputeUpdateSchema(BaseModel):
    priority: Optional[str] = None
    sla_deadline: Optional[datetime] = None
    status: Optional[str] = None
    resolution: Optional[str] = None
    resolution_amount_adjusted: Optional[Decimal] = None
    assigned_to_admin_id: Optional[UUID] = None
    resolved_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    escalation_count: Optional[int] = None

class DisputeResponseSchema(DisputeBaseSchema):
    id: UUID
    priority: str
    sla_deadline: Optional[datetime]
    status: str
    resolution: Optional[str]
    resolution_amount_adjusted: Optional[Decimal]
    assigned_to_admin_id: Optional[UUID]
    resolved_at: Optional[datetime]
    closed_at: Optional[datetime]
    escalation_count: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)