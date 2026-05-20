from redis.asyncio import Redis

from app.core.config import settings


# =========================================================
# REDIS CONNECTION
# =========================================================

redis_client = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=False,
)


# =========================================================
# REDIS HEALTH CHECK
# =========================================================

async def check_redis_connection():

    try:

        await redis_client.ping()

        print("✅ Redis Connected")

    except Exception as e:

        print(f"❌ Redis Connection Failed: {e}")