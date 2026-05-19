from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from core.enums import (
    LoyaltyTier,
    AddressType,
    PreferredLanguage,
    EmergencyContactRelation,
    LoyaltyTransactionType,
    LoyaltyTransactionSource,
)


class CustomerProfileBase(BaseModel):
    loyalty_points: int = 0
    loyalty_tier: LoyaltyTier = LoyaltyTier.BRONZE
    preferred_language: PreferredLanguage = PreferredLanguage.ENGLISH
    emergency_contact: Optional[str] = None


class CustomerProfileCreate(CustomerProfileBase):
    user_id: int


class CustomerProfileUpdate(BaseModel):
    loyalty_points: Optional[int] = None
    loyalty_tier: Optional[LoyaltyTier] = None
    preferred_language: Optional[PreferredLanguage] = None
    emergency_contact: Optional[str] = None


class CustomerProfileResponse(CustomerProfileBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SavedAddressBase(BaseModel):
    address_type: AddressType = AddressType.HOME
    latitude: float
    longitude: float
    address: str


class SavedAddressCreate(SavedAddressBase):
    user_id: int


class SavedAddressUpdate(BaseModel):
    address_type: Optional[AddressType] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    address: Optional[str] = None


class SavedAddressResponse(SavedAddressBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CustomerPreferenceBase(BaseModel):
    notification_enabled: bool = True
    dark_mode: bool = False
    language: PreferredLanguage = PreferredLanguage.ENGLISH


class CustomerPreferenceCreate(CustomerPreferenceBase):
    user_id: int


class CustomerPreferenceUpdate(BaseModel):
    notification_enabled: Optional[bool] = None
    dark_mode: Optional[PreferredLanguage] = None
    language: Optional[PreferredLanguage] = None


class CustomerPreferenceResponse(CustomerPreferenceBase):
    id: int
    user_id: int
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class EmergencyContactBase(BaseModel):
    name: str
    mobile_number: str
    relation: EmergencyContactRelation
    is_primary: bool = False


class EmergencyContactCreate(EmergencyContactBase):
    user_id: int


class EmergencyContactUpdate(BaseModel):
    name: Optional[str] = None
    mobile_number: Optional[str] = None
    relation: Optional[EmergencyContactRelation] = None
    is_primary: Optional[bool] = None


class EmergencyContactResponse(EmergencyContactBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class FavoriteDriverBase(BaseModel):
    driver_id: int
    notes: Optional[str] = None


class FavoriteDriverCreate(FavoriteDriverBase):
    user_id: int


class FavoriteDriverUpdate(BaseModel):
    notes: Optional[str] = None


class FavoriteDriverResponse(FavoriteDriverBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class LoyaltyTransactionBase(BaseModel):
    transaction_type: LoyaltyTransactionType
    source: LoyaltyTransactionSource
    points: int
    description: Optional[str] = None
    reference_id: Optional[int] = None


class LoyaltyTransactionCreate(LoyaltyTransactionBase):
    user_id: int


class LoyaltyTransactionResponse(LoyaltyTransactionBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)