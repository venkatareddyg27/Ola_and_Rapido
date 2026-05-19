from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Float,
    BigInteger,
    Text,
    Enum as SQLEnum,
)
from sqlalchemy.orm import relationship

from core.database import Base
from core.enums import (
    LoyaltyTier,
    AddressType,
    PreferredLanguage,
    EmergencyContactRelation,
    LoyaltyTransactionType,
    LoyaltyTransactionSource,
)


class CustomerProfile(Base):
    __tablename__ = "customer_profiles"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False, unique=True)

    loyalty_points = Column(Integer, default=0, nullable=False)
    loyalty_tier = Column(SQLEnum(LoyaltyTier), default=LoyaltyTier.BRONZE, nullable=False)
    preferred_language = Column(SQLEnum(PreferredLanguage), default=PreferredLanguage.ENGLISH, nullable=False)

    emergency_contact = Column(String(15), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="customer_profile")


class SavedAddress(Base):
    __tablename__ = "saved_addresses"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)

    address_type = Column(SQLEnum(AddressType), default=AddressType.HOME, nullable=False)

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    address = Column(Text, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="saved_addresses")


class CustomerPreference(Base):
    __tablename__ = "customer_preferences"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False, unique=True)

    notification_enabled = Column(Boolean, default=True, nullable=False)
    dark_mode = Column(Boolean, default=False, nullable=False)
    language = Column(SQLEnum(PreferredLanguage), default=PreferredLanguage.ENGLISH, nullable=False)

    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="customer_preferences")


class EmergencyContact(Base):
    __tablename__ = "emergency_contacts"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)

    name = Column(String(100), nullable=False)
    mobile_number = Column(String(15), nullable=False)
    relation = Column(SQLEnum(EmergencyContactRelation), nullable=False)

    is_primary = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="emergency_contacts")


class FavoriteDriver(Base):
    __tablename__ = "favorite_drivers"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    driver_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)

    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship(
        "User",
        foreign_keys=[user_id],
        back_populates="favorite_drivers"
    )

    driver = relationship(
        "User",
        foreign_keys=[driver_id],
        back_populates="favorited_by_customers"
    )


class LoyaltyTransaction(Base):
    __tablename__ = "loyalty_transactions"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)

    transaction_type = Column(SQLEnum(LoyaltyTransactionType), nullable=False)
    source = Column(SQLEnum(LoyaltyTransactionSource), nullable=False)

    points = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)

    reference_id = Column(BigInteger, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="loyalty_transactions")