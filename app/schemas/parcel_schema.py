
 
 
from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
from typing import Optional
 
 
# =========================================================
# PARCEL SCHEMAS
# =========================================================
 
class ParcelBase(BaseModel):
 
    receiver_name: str
    receiver_mobile: str
    pickup_address: str
    delivery_address: str
    package_type: str
    weight_tier: str
    delivery_fee: Decimal
 
 
class ParcelCreate(ParcelBase):
 
    sender_user_id: int
 
 
class ParcelUpdate(BaseModel):
 
    receiver_name: Optional[str] = None
    receiver_mobile: Optional[str] = None
    pickup_address: Optional[str] = None
    delivery_address: Optional[str] = None
    package_type: Optional[str] = None
    weight_tier: Optional[str] = None
    parcel_status: Optional[str] = None
    delivery_fee: Optional[Decimal] = None
 
 
class ParcelResponse(ParcelBase):
 
    id: int
    sender_user_id: int
    parcel_status: str
    created_at: datetime
 
    class Config:
        orm_mode = True
 
 
# =========================================================
# PARCEL TRACKING SCHEMAS
# =========================================================
 
class ParcelTrackingBase(BaseModel):
 
    latitude: Decimal
    longitude: Decimal
    status: str
 
 
class ParcelTrackingCreate(ParcelTrackingBase):
 
    parcel_id: int
 
 
class ParcelTrackingResponse(ParcelTrackingBase):
 
    id: int
    parcel_id: int
    recorded_at: datetime
 
    class Config:
        orm_mode = True
 
 
# =========================================================
# PARCEL ITEM SCHEMAS
# =========================================================
 
class ParcelItemBase(BaseModel):
 
    item_name: str
    quantity: int
    weight: Decimal
    fragile: bool = False
 
 
class ParcelItemCreate(ParcelItemBase):
 
    parcel_id: int
 
 
class ParcelItemUpdate(BaseModel):
 
    item_name: Optional[str] = None
    quantity: Optional[int] = None
    weight: Optional[Decimal] = None
    fragile: Optional[bool] = None
 
 
class ParcelItemResponse(ParcelItemBase):
 
    id: int
    parcel_id: int
 
    class Config:
        orm_mode = True
 
 
# =========================================================
# PARCEL STATUS HISTORY SCHEMAS
# =========================================================
 
class ParcelStatusHistoryBase(BaseModel):
 
    old_status: Optional[str] = None
    new_status: str
    remarks: Optional[str] = None
 
 
class ParcelStatusHistoryCreate(ParcelStatusHistoryBase):
 
    parcel_id: int
 
 
class ParcelStatusHistoryResponse(ParcelStatusHistoryBase):
 
    id: int
    parcel_id: int
    updated_at: datetime
 
    class Config:
        orm_mode = True
 
 
# =========================================================
# PARCEL PROOF SCHEMAS
# =========================================================
 
class ParcelProofBase(BaseModel):
 
    proof_type: str
    proof_url: str
 
 
class ParcelProofCreate(ParcelProofBase):
 
    parcel_id: int
 
 
class ParcelProofResponse(ParcelProofBase):
 
    id: int
    parcel_id: int
    uploaded_at: datetime
 
    class Config:
        orm_mode = True
 
 
# =========================================================
# PARCEL DELIVERY ATTEMPT SCHEMAS
# =========================================================
 
class ParcelDeliveryAttemptBase(BaseModel):
 
    attempt_number: int = 1
    delivery_status: str
    remarks: Optional[str] = None
 
 
class ParcelDeliveryAttemptCreate(ParcelDeliveryAttemptBase):
 
    parcel_id: int
 
 
class ParcelDeliveryAttemptResponse(ParcelDeliveryAttemptBase):
 
    id: int
    parcel_id: int
    attempted_at: datetime
 
    class Config:
        orm_mode = True
 
 
# =========================================================
# PARCEL PRICING SCHEMAS
# =========================================================
 
class ParcelPricingBase(BaseModel):
 
    base_price: Decimal
    weight_charge: Decimal = 0
    fragile_charge: Decimal = 0
    tax_amount: Decimal = 0
    total_amount: Decimal
 
 
class ParcelPricingCreate(ParcelPricingBase):
 
    parcel_id: int
 
 
class ParcelPricingUpdate(BaseModel):
 
    base_price: Optional[Decimal] = None
    weight_charge: Optional[Decimal] = None
    fragile_charge: Optional[Decimal] = None
    tax_amount: Optional[Decimal] = None
    total_amount: Optional[Decimal] = None
 
 
class ParcelPricingResponse(ParcelPricingBase):
 
    id: int
    parcel_id: int
    created_at: datetime
 
    class Config:
        orm_mode = True
 
 
# =========================================================
# PARCEL FEEDBACK SCHEMAS
# =========================================================
 
class ParcelFeedbackBase(BaseModel):
 
    rating: int
    feedback_comment: Optional[str] = None
 
 
class ParcelFeedbackCreate(ParcelFeedbackBase):
 
    parcel_id: int
 
 
class ParcelFeedbackUpdate(BaseModel):
 
    rating: Optional[int] = None
    feedback_comment: Optional[str] = None
 
 
class ParcelFeedbackResponse(ParcelFeedbackBase):
 
    id: int
    parcel_id: int
    created_at: datetime
 
    class Config:
        orm_mode = True
 