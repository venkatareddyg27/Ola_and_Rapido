
 
 
 
from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime,
    Integer,
    BigInteger,
    Text,
    ForeignKey,
    Numeric
)
 
from sqlalchemy.sql import func
 
from app.core.database import Base
 
 
# =========================================================
# TABLE: PARCELS
# Stores parcel bookings
# =========================================================
 
class Parcel(Base):
 
    __tablename__ = "parcels"
 
    id = Column(
        BigInteger,
        primary_key=True,
        index=True
    )
 
    sender_user_id = Column(
        BigInteger,
        ForeignKey("users.id"),
        nullable=False
    )
 
    receiver_name = Column(
        String(255),
        nullable=False
    )
 
    receiver_mobile = Column(
        String(20),
        nullable=False
    )
 
    pickup_address = Column(
        Text,
        nullable=False
    )
 
    delivery_address = Column(
        Text,
        nullable=False
    )
 
    package_type = Column(
        String(100),
        nullable=False
    )
 
    weight_tier = Column(
        String(50),
        nullable=False
    )
 
    parcel_status = Column(
        String(50),
        default="PENDING"
    )
 
    delivery_fee = Column(
        Numeric(10, 2),
        nullable=False
    )
 
    created_at = Column(
        DateTime,
        server_default=func.now()
    )
 
 
# =========================================================
# TABLE: PARCEL_TRACKING
# Stores parcel tracking details
# =========================================================
 
class ParcelTracking(Base):
 
    __tablename__ = "parcel_tracking"
 
    id = Column(
        BigInteger,
        primary_key=True,
        index=True
    )
 
    parcel_id = Column(
        BigInteger,
        ForeignKey("parcels.id"),
        nullable=False
    )
 
    latitude = Column(
        Numeric(10, 8),
        nullable=False
    )
 
    longitude = Column(
        Numeric(11, 8),
        nullable=False
    )
 
    status = Column(
        String(100),
        nullable=False
    )
 
    recorded_at = Column(
        DateTime,
        server_default=func.now()
    )
 
 
# =========================================================
# TABLE: PARCEL_ITEMS
# Stores parcel item details
# =========================================================
 
class ParcelItem(Base):
 
    __tablename__ = "parcel_items"
 
    id = Column(
        BigInteger,
        primary_key=True,
        index=True
    )
 
    parcel_id = Column(
        BigInteger,
        ForeignKey("parcels.id"),
        nullable=False
    )
 
    item_name = Column(
        String(255),
        nullable=False
    )
 
    quantity = Column(
        Integer,
        default=1
    )
 
    weight = Column(
        Numeric(10, 2),
        nullable=False
    )
 
    fragile = Column(
        Boolean,
        default=False
    )
 
 
# =========================================================
# TABLE: PARCEL_STATUS_HISTORY
# Stores parcel status updates history
# =========================================================
 
class ParcelStatusHistory(Base):
 
    __tablename__ = "parcel_status_history"
 
    id = Column(
        BigInteger,
        primary_key=True,
        index=True
    )
 
    parcel_id = Column(
        BigInteger,
        ForeignKey("parcels.id"),
        nullable=False
    )
 
    old_status = Column(
        String(100),
        nullable=True
    )
 
    new_status = Column(
        String(100),
        nullable=False
    )
 
    remarks = Column(
        Text,
        nullable=True
    )
 
    updated_at = Column(
        DateTime,
        server_default=func.now()
    )
 
 
# =========================================================
# TABLE: PARCEL_PROOFS
# Stores delivery proof details
# =========================================================
 
class ParcelProof(Base):
 
    __tablename__ = "parcel_proofs"
 
    id = Column(
        BigInteger,
        primary_key=True,
        index=True
    )
 
    parcel_id = Column(
        BigInteger,
        ForeignKey("parcels.id"),
        nullable=False
    )
 
    proof_type = Column(
        String(100),
        nullable=False
    )
 
    proof_url = Column(
        Text,
        nullable=False
    )
 
    uploaded_at = Column(
        DateTime,
        server_default=func.now()
    )
 
 
# =========================================================
# TABLE: PARCEL_DELIVERY_ATTEMPTS
# Stores failed/success delivery attempts
# =========================================================
 
class ParcelDeliveryAttempt(Base):
 
    __tablename__ = "parcel_delivery_attempts"
 
    id = Column(
        BigInteger,
        primary_key=True,
        index=True
    )
 
    parcel_id = Column(
        BigInteger,
        ForeignKey("parcels.id"),
        nullable=False
    )
 
    attempt_number = Column(
        Integer,
        default=1
    )
 
    delivery_status = Column(
        String(100),
        nullable=False
    )
 
    remarks = Column(
        Text,
        nullable=True
    )
 
    attempted_at = Column(
        DateTime,
        server_default=func.now()
    )
 
 
# =========================================================
# TABLE: PARCEL_PRICING
# Stores parcel pricing details
# =========================================================
 
class ParcelPricing(Base):
 
    __tablename__ = "parcel_pricing"
 
    id = Column(
        BigInteger,
        primary_key=True,
        index=True
    )
 
    parcel_id = Column(
        BigInteger,
        ForeignKey("parcels.id"),
        nullable=False
    )
 
    base_price = Column(
        Numeric(10, 2),
        nullable=False
    )
 
    weight_charge = Column(
        Numeric(10, 2),
        default=0
    )
 
    fragile_charge = Column(
        Numeric(10, 2),
        default=0
    )
 
    tax_amount = Column(
        Numeric(10, 2),
        default=0
    )
 
    total_amount = Column(
        Numeric(10, 2),
        nullable=False
    )
 
    created_at = Column(
        DateTime,
        server_default=func.now()
    )
 
 
# =========================================================
# TABLE: PARCEL_FEEDBACK
# Stores parcel delivery feedback
# =========================================================
 
class ParcelFeedback(Base):
 
    __tablename__ = "parcel_feedback"
 
    id = Column(
        BigInteger,
        primary_key=True,
        index=True
    )
 
    parcel_id = Column(
        BigInteger,
        ForeignKey("parcels.id"),
        nullable=False
    )
 
    rating = Column(
        Integer,
        nullable=False
    )
 
    feedback_comment = Column(
        Text,
        nullable=True
    )
 
    created_at = Column(
        DateTime,
        server_default=func.now()
    )
 