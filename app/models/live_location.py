from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Numeric,
    Integer,
    BigInteger,
    Enum as SAEnum
)

from sqlalchemy.sql import func

from app.core.database import Base
from app.core.enums import UserTypeEnum


class LiveLocation(Base):
    __tablename__ = "live_locations"

    # Primary Key
    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        index=True
    )

    # User Relationships
    user_id = Column(
        BigInteger,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    user_type = Column(
        SAEnum(UserTypeEnum),
        nullable=False
    )

    # GPS Coordinates
    latitude = Column(Numeric(10, 8), nullable=False)

    longitude = Column(Numeric(11, 8), nullable=False)

    accuracy_meters = Column(Numeric(5, 2), nullable=True)

    # Movement Data
    speed_kmh = Column(Numeric(5, 2), nullable=True)

    heading = Column(Integer, nullable=True)

    # Trip Reference
    trip_id = Column(BigInteger, nullable=True, index=True)

    trip_type = Column(String(20), nullable=True)

    # Flags
    is_mocked = Column(Boolean, default=False)

    source = Column(String(20), default="app")

    # Timestamps
    recorded_at = Column(DateTime, nullable=False)

    created_at = Column(
        DateTime,
        server_default=func.now()
    )