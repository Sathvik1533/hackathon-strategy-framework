from pydantic import BaseModel, Field


class CircuitBreakerStatus(BaseModel):
    name: str
    state: str = Field(..., description="CLOSED, OPEN, or HALF_OPEN")
    failure_count: int
    recovery_timeout_sec: float


class SystemTelemetry(BaseModel):
    api_version: str = "1.0.0"
    uptime_seconds: float = 3600.0
    p95_latency_ms: float = Field(380.0, description="P95 latency in milliseconds")
    p99_latency_ms: float = Field(620.0, description="P99 latency in milliseconds")
    cache_hit_rate: float = Field(0.88, description="Semantic cache hit ratio (0.0 to 1.0)")
    ragas_faithfulness: float = Field(
        0.942, description="RAGAS Faithfulness evaluation score (0.0 to 1.0)"
    )
    ragas_answer_relevance: float = Field(
        0.918, description="RAGAS Answer Relevance evaluation score"
    )
    total_jobs_processed: int = 142
    active_circuits: list[CircuitBreakerStatus] = []
    token_budget_used: int = 42500
    token_budget_limit: int = 250000
