from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base
from app.core.config import settings


# =========================================================
# DATABASE URL
# =========================================================

DATABASE_URL = settings.DATABASE_URL


# =========================================================
# ENGINE
# =========================================================

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
)


# =========================================================
# SESSION
# =========================================================

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# =========================================================
# BASE
# =========================================================

Base = declarative_base()


# =========================================================
# DATABASE DEPENDENCY
# =========================================================

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()