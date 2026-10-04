import asyncio
import functools
import logging
import random
import time
from typing import Any, Callable, Optional

import redis.asyncio as aioredis
from src.app.core.config import settings

logger = logging.getLogger("resilience")


# ============================================================================
# 1. EXPONENTIAL BACKOFF WITH FULL JITTER
# ============================================================================
def retry_with_exponential_backoff(
    max_retries: int = 3,
    base_delay: float = 0.5,
    max_delay: float = 10.0,
    retryable_exceptions: tuple = (Exception,),
):
    """
    Retries an async function using exponential backoff with full jitter.
    Formula: delay = min(max_delay, uniform(0, base_delay * (2 ** attempt)))
    Prevents "thundering herd" spikes when external APIs (OpenAI, Anthropic) rate limit.
    """

    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            attempt = 0
            while True:
                try:
                    return await func(*args, **kwargs)
                except retryable_exceptions as exc:
                    attempt += 1
                    if attempt > max_retries:
                        logger.error(
                            f"Exceeded max retries ({max_retries}) for {func.__name__}. Error: {exc}"
                        )
                        raise

                    # Exponential backoff with random full jitter
                    sleep_time = min(max_delay, random.uniform(0, base_delay * (2**attempt)))
                    logger.warning(
                        f"Attempt {attempt}/{max_retries} failed for {func.__name__}: {exc}. "
                        f"Retrying in {sleep_time:.2f}s..."
                    )
                    await asyncio.sleep(sleep_time)

        return wrapper

    return decorator


# ============================================================================
# 2. CIRCUIT BREAKER PATTERN
# ============================================================================
class CircuitBreakerOpenException(Exception):
    """Raised when circuit breaker is in OPEN state, stopping calls immediately."""

    pass


class CircuitBreaker:
    """
    Protects downstream systems (LLMs, external scrapers, payment gateways).
    States:
      - CLOSED: Normal operation, requests pass through.
      - OPEN: Failures exceeded threshold; fails fast immediately without calling downstream.
      - HALF_OPEN: Trial period after recovery timeout; allows 1 request to verify health.
    """

    def __init__(self, failure_threshold: int = 5, recovery_timeout: float = 30.0):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.state = "CLOSED"
        self.last_state_change = time.time()

    async def call(self, func: Callable, *args, **kwargs) -> Any:
        now = time.time()

        if self.state == "OPEN":
            if now - self.last_state_change > self.recovery_timeout:
                self.state = "HALF_OPEN"
                self.last_state_change = now
                logger.info(
                    "CircuitBreaker transition: OPEN -> HALF_OPEN (probing downstream service)"
                )
            else:
                raise CircuitBreakerOpenException(
                    f"Circuit breaker is OPEN. Fast-failing to protect downstream service. "
                    f"Retry in {int(self.recovery_timeout - (now - self.last_state_change))}s."
                )

        try:
            result = await func(*args, **kwargs)
            if self.state in ("HALF_OPEN", "CLOSED"):
                self.failure_count = 0
                self.state = "CLOSED"
            return result
        except Exception as e:
            self.failure_count += 1
            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
                self.last_state_change = now
                logger.error(
                    f"CircuitBreaker transition -> OPEN! Failures: {self.failure_count}. Error: {e}"
                )
            raise


# ============================================================================
# 3. IDEMPOTENCY KEY GUARD (REDIS DISTRIBUTED LOCK)
# ============================================================================
class IdempotencyGuard:
    """
    Ensures an operation (payment, video render, credit deduction) runs exactly once,
    even if the frontend or user submits the same request multiple times concurrently.
    """

    def __init__(self, redis_url: str = settings.REDIS_URL):
        self.redis = aioredis.from_url(redis_url, decode_responses=True)

    async def acquire_lock(self, idempotency_key: str, ttl_seconds: int = 120) -> bool:
        """
        Uses Redis SETNX (set if not exists) with TTL.
        Returns True if acquired (first time), False if already processed or in-flight.
        """
        key = f"idempotency:{idempotency_key}"
        acquired = await self.redis.set(key, "PROCESSING", nx=True, ex=ttl_seconds)
        return bool(acquired)

    async def set_result(self, idempotency_key: str, result_payload: str, ttl_seconds: int = 86400):
        """Stores final completed payload so duplicate requests receive cached result instantly."""
        key = f"idempotency:result:{idempotency_key}"
        await self.redis.set(key, result_payload, ex=ttl_seconds)

    async def get_cached_result(self, idempotency_key: str) -> Optional[str]:
        return await self.redis.get(f"idempotency:result:{idempotency_key}")
