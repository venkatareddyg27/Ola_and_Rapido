import logging

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)

from sqlalchemy.orm import declarative_base

from app.core.config import settings


# =====================================================
# DISABLE SQL LOGS
# =====================================================

logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

# =====================================================
# DATABASE URL
# =====================================================

DATABASE_URL = settings.DATABASE_URL

# =====================================================
# ENGINE
# =====================================================

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)

# =====================================================
# SESSION
# =====================================================

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

# =====================================================
# BASE
# =====================================================

Base = declarative_base()

# =====================================================
# DB DEPENDENCY
# =====================================================

async def get_db():

    async with AsyncSessionLocal() as session:

        yield session