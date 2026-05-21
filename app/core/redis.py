# redis.py

import redis.asyncio as redis

from app.core.config import (
    settings
)

# =========================================================
# REDIS CLIENT
# =========================================================

redis_client = redis.from_url(

    settings.REDIS_URL,

    decode_responses=True
)

# =========================================================
# REDIS HEALTH CHECK
# =========================================================

async def check_redis():

    try:

        await redis_client.ping()

        print(
            "✅ Redis Connected"
        )

    except Exception as e:

        print(
            f"❌ Redis Error: {e}"
        )