import uuid
from datetime import datetime

from sqlalchemy import ( Column, String, Numeric, Integer, Boolean, DateTime, ForeignKey, Enum )

from sqlalchemy.dialects.postgresql import ( UUID, ARRAY, JSONB )

from sqlalchemy.orm import relationship

from app.core.database import Base

from app.core.enums import ( DiscountType )


class PromoCode(Base):

    __tablename__ = "promo_codes"

    id = Column( UUID(as_uuid=True), primary_key=True, default=uuid.uuid4 )

    code = Column( String(20), unique=True, nullable=False )

    discount_type = Column( Enum(DiscountType), nullable=False )

    discount_value = Column( Numeric(10, 2), nullable=False )

    max_discount = Column( Numeric(10, 2) )

    min_order = Column( Numeric(10, 2) )

    usage_limit = Column( Integer )

    used_count = Column( Integer, default=0 )

    valid_from = Column( DateTime, nullable=False )

    valid_until = Column( DateTime, nullable=False )

    service_types = Column( ARRAY(String) )

    active = Column( Boolean, default=True )

    created_by = Column( UUID(as_uuid=True), ForeignKey("users.id") )

    created_at = Column( DateTime, default=datetime.utcnow )

    updated_at = Column( DateTime, default=datetime.utcnow, onupdate=datetime.utcnow )

    creator = relationship( "User", foreign_keys=[created_by], back_populates="promo_codes" )

class SurgeZone(Base):

    __tablename__ = "surge_zones"

    id = Column( UUID(as_uuid=True), primary_key=True, default=uuid.uuid4 )

    zone_name = Column( String(100), nullable=False )

    city = Column( String(100), nullable=False )

    polygon = Column( JSONB, nullable=False )

    multiplier = Column( Numeric(4, 2), default=1.0 )

    active = Column( Boolean, default=True )

    created_by = Column( UUID(as_uuid=True), ForeignKey("users.id"), nullable=False )

    created_at = Column( DateTime, default=datetime.utcnow )

    updated_at = Column( DateTime, default=datetime.utcnow, onupdate=datetime.utcnow )

    creator = relationship( "User", foreign_keys=[created_by], back_populates="surge_zones")


class AuditLog(Base):

    __tablename__ = "audit_logs"

    id = Column( UUID(as_uuid=True), primary_key=True, default=uuid.uuid4 )

    actor_id = Column( UUID(as_uuid=True), ForeignKey("users.id"), nullable=False )

    action = Column( String(100), nullable=False )

    entity_type = Column( String(100), nullable=False )

    entity_id = Column( String(100), nullable=False)

    old_value = Column( JSONB )

    new_value = Column( JSONB )

    ip_address = Column( String(50) )

    created_at = Column( DateTime, default=datetime.utcnow )

    actor = relationship( "User", foreign_keys=[actor_id], back_populates="audit_logs" )