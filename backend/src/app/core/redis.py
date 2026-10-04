"""Redis Unified Infrastructure & Key Topology Manager.

Defines standardized key namespaces for semantic caching, task queues,
idempotency locks, rate limits, and real-time Server-Sent Events (SSE)
Pub/Sub channels.
"""

from src.app.core.config import settings

try:
    import redis.asyncio as aioredis

    redis_pool = aioredis.ConnectionPool.from_url(
        settings.REDIS_URL, max_connections=20, decode_responses=True
    )

    def get_redis_client() -> aioredis.Redis:
        """Returns an async Redis client from the shared connection pool."""
        return aioredis.Redis(connection_pool=redis_pool)

except ImportError:
    # In-memory mock async redis client for host testing environments without redis-py
    class MockRedisPubSub:
        async def subscribe(self, channel: str):
            pass

        async def listen(self):
            if False:
                yield

    class MockRedis:
        def __init__(self):
            self.store = {}

        async def get(self, key: str):
            return self.store.get(key)

        async def set(self, key: str, value: str, ex=None, nx=False):
            if nx and key in self.store:
                return False
            self.store[key] = value
            return True

        async def setex(self, key: str, time: int, value: str):
            self.store[key] = value

        async def publish(self, channel: str, message: str):
            pass

        def pubsub(self):
            return MockRedisPubSub()

    redis_pool = None

    def get_redis_client():
        return MockRedis()


class RedisKeyTopology:
    """Standardized Redis key schema to eliminate collisions across agent workflows."""

    @staticmethod
    def semantic_cache(query_hash: str) -> str:
        """cache:semantic:<16-char-hash> -> JSON string of cached agent output"""
        return f"cache:semantic:{query_hash}"

    @staticmethod
    def job_channel(job_id: str) -> str:
        """channel:jobs:<uuid> -> Redis Pub/Sub channel for live SSE streaming"""
        return f"channel:jobs:{job_id}"

    @staticmethod
    def job_state(job_id: str) -> str:
        """state:jobs:<uuid> -> Latest progress snapshot for reconnecting clients"""
        return f"state:jobs:{job_id}"

    @staticmethod
    def idempotency_lock(key: str) -> str:
        """lock:idempotency:<unique-key> -> Distributed mutex lock (TTL 120s)"""
        return f"lock:idempotency:{key}"

    @staticmethod
    def idempotency_result(key: str) -> str:
        """result:idempotency:<unique-key> -> Cached response payload (TTL 24h)"""
        return f"result:idempotency:{key}"

    @staticmethod
    def rate_limit(user_or_ip: str, window_minute: int) -> str:
        """ratelimit:<id>:<minute-timestamp> -> Sliding-window counter"""
        return f"ratelimit:{user_or_ip}:{window_minute}"

    @staticmethod
    def session_token_budget(session_id: str) -> str:
        """budget:tokens:<session-id> -> Cumulative token consumption counter"""
        return f"budget:tokens:{session_id}"
