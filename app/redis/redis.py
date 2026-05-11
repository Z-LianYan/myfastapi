from app.core.config import settings
import redis.asyncio as redis

class RedisManager:
    def __init__(self):
        self.db0 = None
        self.db1 = None

    async def connect(self):
        self.db0 = redis.from_url(
            settings.REDIS_URL0,
            decode_responses=True
        )

        self.db1 = redis.from_url(
            settings.REDIS_URL1,
            decode_responses=True
        )

        await self.db0.ping()
        await self.db1.ping()

    async def close(self):
        if self.db0:
            await self.db0.close()

        if self.db1:
            await self.db1.close()


redis_manager = RedisManager()