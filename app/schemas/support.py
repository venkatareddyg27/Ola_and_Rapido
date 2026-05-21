# =========================================================
# SUPPORT SCHEMAS
# =========================================================

from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID

from pydantic import BaseModel

from app.core.enums import (
    DisputeCategory,
    DisputeStatus,
    DisputePriority
)


# =========================================================
# RATING SCHEMAS
# =========================================================

class RatingBase(BaseModel):
    trip_id: Optional[UUID] = None
    rental_id: Optional[UUID] = None
    rater_id: UUID
    ratee_id: UUID
    score: int
    comment: Optional[str] = None


class RatingCreate(RatingBase):
    pass


class RatingUpdate(BaseModel):
    score: Optional[int] = None
    comment: Optional[str] = None


class RatingResponse(RatingBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


# =========================================================
# NOTIFICATION SCHEMAS
# =========================================================

class NotificationBase(BaseModel):
    user_id: UUID
    title: str
    body: str
    type: str
    data: Optional[Dict[str, Any]] = None


class NotificationCreate(NotificationBase):
    pass


class NotificationUpdate(BaseModel):
    read_at: Optional[datetime] = None


class NotificationResponse(NotificationBase):
    id: UUID
    read_at: Optional[datetime]
    created_at: datetime
class NotificationMarkReadRequest(BaseModel):
    notification_id: UUID
    read_at: datetime
    class Config:
        from_attributes = True


# =========================================================
# DISPUTE SCHEMAS
# =========================================================

class DisputeBase(BaseModel):
    trip_id: Optional[UUID] = None
    rental_id: Optional[UUID] = None
    category: DisputeCategory
    description: str
    priority: DisputePriority = DisputePriority.MEDIUM


class DisputeCreate(DisputeBase):
    user_id: UUID


class DisputeUpdate(BaseModel):
    status: Optional[DisputeStatus] = None
    priority: Optional[DisputePriority] = None
    resolution: Optional[str] = None
    resolved_by: Optional[UUID] = None
    resolved_at: Optional[datetime] = None


class DisputeResponse(DisputeBase):
    id: UUID
    user_id: UUID
    resolved_by: Optional[UUID]
    status: DisputeStatus
    resolution: Optional[str]
    created_at: datetime
    resolved_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True