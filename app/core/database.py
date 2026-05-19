from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker
)

from sqlalchemy.orm import declarative_base

from core.config import settings


# =========================================================
# DATABASE URL
# =========================================================

DATABASE_URL = settings.DATABASE_URL


# =========================================================
# ASYNC ENGINE
# =========================================================

engine = create_async_engine(
    DATABASE_URL,
    echo=True
)


# =========================================================
# ASYNC SESSION
# =========================================================

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


# =========================================================
# BASE
# =========================================================

Base = declarative_base()


# =========================================================
# DATABASE DEPENDENCY
# =========================================================

async def get_db():

    async with AsyncSessionLocal() as session:
        yield session