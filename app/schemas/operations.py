import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional, List, Dict, Any
from pydantic import (BaseModel,ConfigDict)
from app.core.enums import (DiscountType)


class PromoCodeBase(BaseModel):
    code: str
    discount_type: DiscountType
    discount_value: Decimal
    max_discount: Optional[Decimal] = None
    min_order: Optional[Decimal] = None
    usage_limit: Optional[int] = None
    valid_from: datetime
    valid_until: datetime
    service_types: Optional[List[str]] = []

class PromoCodeCreate(PromoCodeBase):
    pass

class PromoCodeUpdate(BaseModel):
    code: Optional[str] = None
    discount_type: Optional[DiscountType] = None
    discount_value: Optional[Decimal] = None
    max_discount: Optional[Decimal] = None
    min_order: Optional[Decimal] = None
    usage_limit: Optional[int] = None
    valid_from: Optional[datetime] = None
    valid_until: Optional[datetime] = None
    service_types: Optional[List[str]] = None
    active: Optional[bool] = None


class PromoCodeResponse(PromoCodeBase):
    id: uuid.UUID
    used_count: int
    active: bool
    created_by: Optional[uuid.UUID] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class PromoApplyRequest(BaseModel):
    code: str
    order_amount: Decimal
    service_type: str


class PromoApplyResponse(BaseModel):
    promo_code: str
    discount_amount: Decimal
    final_amount: Decimal


class SurgeZoneBase(BaseModel):
    zone_name: str
    city: str
    polygon: Dict[str, Any]
    multiplier: Decimal = Decimal("1.0")


class SurgeZoneCreate(SurgeZoneBase):
    pass


class SurgeZoneUpdate(BaseModel):
    zone_name: Optional[str] = None
    city: Optional[str] = None
    polygon: Optional[Dict[str, Any]] = None
    multiplier: Optional[Decimal] = None
    active: Optional[bool] = None


class SurgeZoneResponse(SurgeZoneBase):
    id: uuid.UUID
    active: bool
    created_by: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AuditLogBase(BaseModel):
    action: str
    entity_type: str
    entity_id: str
    old_value: Optional[Dict[str, Any]] = None
    new_value: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = None


class AuditLogCreate(AuditLogBase):
    actor_id: uuid.UUID


class AuditLogResponse(AuditLogBase):
    id: uuid.UUID
    actor_id: uuid.UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
    


class PromoCreate(BaseModel):
    code: str
    discount_type: DiscountType
    discount_value: Decimal
    max_discount: Optional[Decimal] = None
    min_order: Optional[Decimal] = None
    usage_limit: Optional[int] = None
    valid_from: datetime
    valid_until: datetime
    service_types: Optional[list[str]] = []


class PromoResponse(BaseModel):
    id: uuid.UUID
    code: str
    discount_type: DiscountType
    discount_value: Decimal
    max_discount: Optional[Decimal] = None
    min_order: Optional[Decimal] = None
    usage_limit: Optional[int] = None
    used_count: int
    valid_from: datetime
    valid_until: datetime
    service_types: Optional[list[str]] = []
    active: bool
    created_by: Optional[uuid.UUID] = None
    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )