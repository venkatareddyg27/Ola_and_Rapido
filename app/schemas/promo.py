
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict

from app.models.promo import CouponType, CampaignStatus


# =========================================================
# PROMO CAMPAIGN SCHEMAS
# =========================================================

class PromoCampaignBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: CampaignStatus = CampaignStatus.ACTIVE
    start_date: datetime
    end_date: datetime


class PromoCampaignCreate(PromoCampaignBase):
    pass


class PromoCampaignUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[CampaignStatus] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class PromoCampaignResponse(PromoCampaignBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# =========================================================
# COUPON SCHEMAS
# =========================================================

class CouponBase(BaseModel):
    campaign_id: Optional[int] = None
    code: str
    coupon_type: CouponType
    discount_value: float
    min_order_amount: float = 0
    usage_limit: int = 1
    expires_at: Optional[datetime] = None
    is_active: bool = True


class CouponCreate(CouponBase):
    pass


class CouponUpdate(BaseModel):
    discount_value: Optional[float] = None
    min_order_amount: Optional[float] = None
    usage_limit: Optional[int] = None
    expires_at: Optional[datetime] = None
    is_active: Optional[bool] = None


class CouponResponse(CouponBase):
    id: int
    used_count: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# =========================================================
# COUPON USAGE SCHEMAS
# =========================================================

class CouponUsageBase(BaseModel):
    coupon_id: int
    user_id: int
    order_id: Optional[int] = None
    discount_amount: float


class CouponUsageCreate(CouponUsageBase):
    pass


class CouponUsageResponse(CouponUsageBase):
    id: int
    used_at: datetime

    model_config = ConfigDict(from_attributes=True)


# =========================================================
# REFERRAL CODE SCHEMAS
# =========================================================

class ReferralCodeBase(BaseModel):
    user_id: int
    code: str
    is_active: bool = True


class ReferralCodeCreate(ReferralCodeBase):
    pass


class ReferralCodeUpdate(BaseModel):
    is_active: Optional[bool] = None


class ReferralCodeResponse(ReferralCodeBase):
    id: int
    total_referrals: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# =========================================================
# REFERRAL REWARD SCHEMAS
# =========================================================

class ReferralRewardBase(BaseModel):
    referral_code_id: int
    referrer_user_id: int
    referred_user_id: int
    reward_amount: float
    is_claimed: bool = False


class ReferralRewardCreate(ReferralRewardBase):
    pass


class ReferralRewardUpdate(BaseModel):
    is_claimed: Optional[bool] = None


class ReferralRewardResponse(ReferralRewardBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# =========================================================
# CAMPAIGN BANNER SCHEMAS
# =========================================================

class CampaignBannerBase(BaseModel):
    campaign_id: int
    title: str
    image_url: str
    redirect_url: Optional[str] = None
    priority: int = 1
    is_active: bool = True


class CampaignBannerCreate(CampaignBannerBase):
    pass


class CampaignBannerUpdate(BaseModel):
    title: Optional[str] = None
    image_url: Optional[str] = None
    redirect_url: Optional[str] = None
    priority: Optional[int] = None
    is_active: Optional[bool] = None


class CampaignBannerResponse(CampaignBannerBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# =========================================================
# NESTED RESPONSE SCHEMAS
# =========================================================

class PromoCampaignWithCoupons(PromoCampaignResponse):
    coupons: List[CouponResponse] = []
    banners: List["CampaignBannerResponse"] = []


class CouponWithUsages(CouponResponse):
    usages: List[CouponUsageResponse] = []


class ReferralCodeWithRewards(ReferralCodeResponse):
    rewards: List[ReferralRewardResponse] = []