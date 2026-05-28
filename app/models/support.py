import uuid
from datetime import datetime
from sqlalchemy import Column, Enum, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.core.enums import DisputeCategory, DisputeStatus, DisputePriority



class Rating(Base):
    __tablename__ = "ratings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trip_id = Column(UUID(as_uuid=True), ForeignKey("trips.id"))
    rental_id = Column(UUID(as_uuid=True), ForeignKey("rentals.id"))
    rater_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    ratee_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    score = Column(Integer, nullable=False)
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    trip = relationship("Trip", back_populates="ratings")
    rental = relationship("Rental", back_populates="ratings")
    rater = relationship("User", foreign_keys=[rater_id], back_populates="ratings_given")
    ratee = relationship("User", foreign_keys=[ratee_id], back_populates="ratings_received")


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    title = Column(Text, nullable=False)
    body = Column(Text, nullable=False)
    type = Column(String(50), nullable=False)
    data = Column(JSONB)
    read_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="notifications")


class Dispute(Base):
    __tablename__ = "disputes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    resolved_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    trip_id = Column(UUID(as_uuid=True), ForeignKey("trips.id"), nullable=True)
    rental_id = Column(UUID(as_uuid=True), ForeignKey("rentals.id"), nullable=True)
    deduction_id = Column(UUID(as_uuid=True), ForeignKey("rental_deductions.id"), nullable=True)
    category = Column(Enum(DisputeCategory), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(Enum(DisputeStatus), default=DisputeStatus.OPEN, nullable=False)
    priority = Column(Enum(DisputePriority), default=DisputePriority.MEDIUM, nullable=False)
    resolution = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    resolved_at = Column(DateTime)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", foreign_keys=[user_id], back_populates="disputes")
    resolver = relationship("User", foreign_keys=[resolved_by], back_populates="resolved_disputes")
    trip = relationship("Trip", back_populates="disputes")
    rental = relationship("Rental", back_populates="disputes")
   