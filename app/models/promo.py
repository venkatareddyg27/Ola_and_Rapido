
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Float,
    Text,
    Enum,
)
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.core.enums import (
    CampaignStatus,
    CouponType,)

# =========================================================
# PROMO CAMPAIGNS
# =========================================================

class PromoCampaign(Base):
    __tablename__ = "promo_campaigns"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)

    status = Column(
        Enum(CampaignStatus),
        default=CampaignStatus.ACTIVE,
        nullable=False
    )

    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    coupons = relationship(
        "Coupon",
        back_populates="campaign",
        cascade="all, delete-orphan"
    )

    banners = relationship(
        "CampaignBanner",
        back_populates="campaign",
        cascade="all, delete-orphan"
    )


# =========================================================
# COUPONS
# =========================================================

class Coupon(Base):
    __tablename__ = "coupons"

    id = Column(Integer, primary_key=True, index=True)

    campaign_id = Column(
        Integer,
        ForeignKey("promo_campaigns.id"),
        nullable=True
    )

    code = Column(String(50), unique=True, nullable=False)

    coupon_type = Column(
        Enum(CouponType),
        nullable=False
    )

    discount_value = Column(Float, nullable=False)

    min_order_amount = Column(Float, default=0)

    usage_limit = Column(Integer, default=1)

    used_count = Column(Integer, default=0)

    is_active = Column(Boolean, default=True)

    expires_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    campaign = relationship(
        "PromoCampaign",
        back_populates="coupons"
    )

    usages = relationship(
        "CouponUsage",
        back_populates="coupon",
        cascade="all, delete-orphan"
    )


# =========================================================
# COUPON USAGES
# =========================================================

class CouponUsage(Base):
    __tablename__ = "coupon_usages"

    id = Column(Integer, primary_key=True, index=True)

    coupon_id = Column(
        Integer,
        ForeignKey("coupons.id"),
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    order_id = Column(Integer, nullable=True)

    discount_amount = Column(Float, nullable=False)

    used_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    coupon = relationship(
        "Coupon",
        back_populates="usages"
    )

    user = relationship(
        "User",
        back_populates="coupon_usages"
    )


# =========================================================
# REFERRAL CODES
# =========================================================

class ReferralCode(Base):
    __tablename__ = "referral_codes"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    code = Column(String(50), unique=True, nullable=False)

    total_referrals = Column(Integer, default=0)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship(
        "User",
        back_populates="referral_codes"
    )

    rewards = relationship(
        "ReferralReward",
        back_populates="referral_code",
        cascade="all, delete-orphan"
    )


# =========================================================
# REFERRAL REWARDS
# =========================================================

class ReferralReward(Base):
    __tablename__ = "referral_rewards"

    id = Column(Integer, primary_key=True, index=True)

    referral_code_id = Column(
        Integer,
        ForeignKey("referral_codes.id"),
        nullable=False
    )

    referrer_user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    referred_user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    reward_amount = Column(Float, nullable=False)

    is_claimed = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    referral_code = relationship(
        "ReferralCode",
        back_populates="rewards"
    )

    referrer = relationship(
        "User",
        foreign_keys=[referrer_user_id]
    )

    referred_user = relationship(
        "User",
        foreign_keys=[referred_user_id]
    )


# =========================================================
# CAMPAIGN BANNERS
# =========================================================

class CampaignBanner(Base):
    __tablename__ = "campaign_banners"

    id = Column(Integer, primary_key=True, index=True)

    campaign_id = Column(
        Integer,
        ForeignKey("promo_campaigns.id"),
        nullable=False
    )

    title = Column(String(150), nullable=False)

    image_url = Column(String(500), nullable=False)

    redirect_url = Column(String(500), nullable=True)

    priority = Column(Integer, default=1)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    campaign = relationship(
        "PromoCampaign",
        back_populates="banners"
    )