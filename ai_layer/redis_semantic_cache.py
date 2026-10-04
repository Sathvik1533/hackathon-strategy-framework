import hashlib
import json

import redis.asyncio as aioredis


class SemanticCache:
    def __init__(self, redis_url: str = "redis://localhost:6379/1"):
        self.redis = aioredis.from_url(redis_url, decode_responses=True)

    async def get(self, query: str) -> dict | None:
        """Sub-10ms exact / normalized hash cache lookup"""
        query_key = f"cache:query:{hashlib.sha256(query.strip().lower().encode()).hexdigest()[:16]}"
        cached = await self.redis.get(query_key)
        if cached:
            return json.loads(cached)
        return None

    async def set(self, query: str, response: dict, ttl_seconds: int = 86400):
        query_key = f"cache:query:{hashlib.sha256(query.strip().lower().encode()).hexdigest()[:16]}"
        await self.redis.setex(query_key, ttl_seconds, json.dumps(response))
