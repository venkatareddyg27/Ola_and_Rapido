from uuid import UUID
from decimal import Decimal
from datetime import datetime
from typing import Optional
from pydantic import (BaseModel,ConfigDict)


class UserSuspendRequest(BaseModel):
    suspend: bool
    reason: Optional[str] = None




class DisputeResolveRequest(BaseModel):
    resolution_type: str
    refund_amount: Optional[Decimal] = None
    admin_notes: Optional[str] = None



class SurgeOverrideRequest(BaseModel):
    zone_id: UUID
    multiplier: Decimal
    duration_minutes: int


class BroadcastNotificationRequest(BaseModel):

    title: str
    message: str
    target_segment: str


class LiveOpsResponse(BaseModel):
    active_drivers: int
    live_trips: int
    demand_supply_ratio: float


class FinanceSummaryResponse(BaseModel):
    total_revenue: Decimal
    commissions: Decimal
    payouts: Decimal
    refunds: Decimal


class AnalyticsResponse(BaseModel):
    total_users: int
    total_trips: int
    top_zones: list[str]
    peak_hours: list[str]


class AdminUserResponse(BaseModel):
    id: UUID
    full_name: str
    email: str
    role: str
    status: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)