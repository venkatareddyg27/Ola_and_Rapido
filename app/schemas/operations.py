import uuid

from datetime import datetime

from decimal import Decimal

from typing import (
    Optional,
    List,
    Dict,
    Any
)

from pydantic import (
    BaseModel,
    ConfigDict
)

from app.core.enums import (
    DiscountType
)


# =========================================================
# PROMO CODE BASE
# =========================================================

class PromoCodeBase(BaseModel):

    code: str

    description: Optional[str] = None

    discount_type: DiscountType

    discount_value: Decimal

    max_discount: Optional[
        Decimal
    ] = None

    min_order: Optional[
        Decimal
    ] = None

    usage_limit: Optional[
        int
    ] = None

    valid_from: datetime

    valid_until: datetime

    service_types: Optional[
        List[str]
    ] = []


# =========================================================
# PROMO CREATE
# =========================================================

class PromoCodeCreate(
    PromoCodeBase
):
    pass


# =========================================================
# PROMO UPDATE
# =========================================================

class PromoCodeUpdate(
    BaseModel
):

    code: Optional[str] = None

    description: Optional[
        str
    ] = None

    discount_type: Optional[
        DiscountType
    ] = None

    discount_value: Optional[
        Decimal
    ] = None

    max_discount: Optional[
        Decimal
    ] = None

    min_order: Optional[
        Decimal
    ] = None

    usage_limit: Optional[
        int
    ] = None

    valid_from: Optional[
        datetime
    ] = None

    valid_until: Optional[
        datetime
    ] = None

    service_types: Optional[
        List[str]
    ] = None

    active: Optional[
        bool
    ] = None


# =========================================================
# PROMO RESPONSE
# =========================================================

class PromoCodeResponse(
    PromoCodeBase
):

    id: uuid.UUID

    used_count: int

    active: bool

    created_by: Optional[
        uuid.UUID
    ] = None

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# APPLY PROMO REQUEST
# =========================================================

class PromoApplyRequest(
    BaseModel
):

    code: str

    order_amount: Decimal

    service_type: str


# =========================================================
# APPLY PROMO RESPONSE
# =========================================================

class PromoApplyResponse(
    BaseModel
):

    promo_code: str

    discount_amount: Decimal

    final_amount: Decimal


# =========================================================
# SURGE ZONE BASE
# =========================================================

class SurgeZoneBase(
    BaseModel
):

    zone_name: str

    city: str

    polygon: Dict[str, Any]

    multiplier: Decimal = (
        Decimal("1.0")
    )


# =========================================================
# SURGE ZONE CREATE
# =========================================================

class SurgeZoneCreate(
    SurgeZoneBase
):
    pass


# =========================================================
# SURGE ZONE UPDATE
# =========================================================

class SurgeZoneUpdate(
    BaseModel
):

    zone_name: Optional[
        str
    ] = None

    city: Optional[
        str
    ] = None

    polygon: Optional[
        Dict[str, Any]
    ] = None

    multiplier: Optional[
        Decimal
    ] = None

    active: Optional[
        bool
    ] = None


# =========================================================
# SURGE ZONE RESPONSE
# =========================================================

class SurgeZoneResponse(
    SurgeZoneBase
):

    id: uuid.UUID

    active: bool

    created_by: uuid.UUID

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# AUDIT LOG BASE
# =========================================================

class AuditLogBase(
    BaseModel
):

    action: str

    entity_type: str

    entity_id: str

    old_value: Optional[
        Dict[str, Any]
    ] = None

    new_value: Optional[
        Dict[str, Any]
    ] = None

    ip_address: Optional[
        str
    ] = None


# =========================================================
# AUDIT LOG CREATE
# =========================================================

class AuditLogCreate(
    AuditLogBase
):

    actor_id: uuid.UUID


# =========================================================
# AUDIT LOG RESPONSE
# =========================================================

class AuditLogResponse(
    AuditLogBase
):

    id: uuid.UUID

    actor_id: uuid.UUID

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# SIMPLE PROMO CREATE
# =========================================================

class PromoCreate(
    BaseModel
):

    code: str

    description: Optional[
        str
    ] = None

    discount_type: DiscountType

    discount_value: Decimal

    max_discount: Optional[
        Decimal
    ] = None

    min_order: Optional[
        Decimal
    ] = None

    usage_limit: Optional[
        int
    ] = None

    valid_from: datetime

    valid_until: datetime

    service_types: Optional[
        List[str]
    ] = []


# =========================================================
# SIMPLE PROMO RESPONSE
# =========================================================

class PromoResponse(
    BaseModel
):

    id: uuid.UUID

    code: str

    description: Optional[
        str
    ] = None

    discount_type: DiscountType

    discount_value: Decimal

    max_discount: Optional[
        Decimal
    ] = None

    min_order: Optional[
        Decimal
    ] = None

    usage_limit: Optional[
        int
    ] = None

    used_count: int

    valid_from: datetime

    valid_until: datetime

    service_types: Optional[
        List[str]
    ] = []

    active: bool

    created_by: Optional[
        uuid.UUID
    ] = None

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )