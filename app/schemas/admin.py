# schemas/admin.py
from uuid import UUID
from datetime import datetime
from typing import Optional, Any
from enum import Enum
from pydantic import BaseModel, ConfigDict


class ActionTypeEnum(str, Enum):
    create = "create"
    update = "update"
    delete = "delete"
    ban = "ban"
    unban = "unban"
    refund = "refund"
    escalate = "escalate"
    resolve = "resolve"
    assign = "assign"
    export = "export"


# =====================================================
# AdminLog Schemas
# =====================================================

class AdminLogCreateSchema(BaseModel):
    admin_user_id: UUID
    action_type: ActionTypeEnum
    target_user_id: Optional[UUID] = None
    target_entity_type: Optional[str] = None
    target_entity_id: Optional[UUID] = None
    old_value: Optional[Any] = None
    new_value: Optional[Any] = None
    reason: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None


class AdminLogResponseSchema(AdminLogCreateSchema):
    id: UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# =====================================================
# SystemConfig Schemas
# =====================================================

class SystemConfigCreateSchema(BaseModel):
    config_key: str
    config_value: Any
    data_type: Optional[str] = "string"
    description: Optional[str] = None
    updated_by: Optional[UUID] = None


class SystemConfigUpdateSchema(BaseModel):
    config_value: Optional[Any] = None
    data_type: Optional[str] = None
    description: Optional[str] = None
    updated_by: Optional[UUID] = None


class SystemConfigResponseSchema(SystemConfigCreateSchema):
    id: UUID
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)