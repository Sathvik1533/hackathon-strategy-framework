import asyncio
import json
import uuid
from collections.abc import AsyncGenerator

from src.app.core.redis import get_redis_client

redis_client = get_redis_client()


class JobService:
    @staticmethod
    async def enqueue_job(task_type: str, payload: dict) -> str:
        job_id = str(uuid.uuid4())

        # In a full Celery setup: execute_agent_job.delay(job_id, payload)
        # Background fallback worker inside FastAPI for fast standalone demo:
        asyncio.create_task(JobService._run_simulated_agent_job(job_id, task_type, payload))
        return job_id

    @staticmethod
    async def _run_simulated_agent_job(job_id: str, task_type: str, payload: dict):
        channel = f"job_channel:{job_id}"

        async def publish(pct: int, log_msg: str, final_res=None):
            event = {
                "status": "completed" if pct == 100 else "processing",
                "percent": pct,
                "log": log_msg,
                "result": final_res,
            }
            await redis_client.publish(channel, json.dumps(event))
            await redis_client.setex(f"job_state:{job_id}", 3600, json.dumps(event))

        await asyncio.sleep(0.5)
        await publish(15, f"Initializing {task_type} workspace & loading dependencies...")
        await asyncio.sleep(1.0)
        await publish(40, "Executing LangGraph supervisor routing & tool validation...")
        await asyncio.sleep(1.2)
        await publish(75, "Running pgvector hybrid search & semantic context synthesis...")
        await asyncio.sleep(1.0)
        await publish(95, "Validating output against Pydantic schema & security guardrails...")
        await asyncio.sleep(0.8)

        sample_output = {
            "summary": f"Completed {task_type} successfully.",
            "metrics": {"faithfulness": 0.94, "latency_ms": 380},
            "artifacts": ["output_report.json"],
        }
        await publish(100, "Job completed with zero errors.", sample_output)

    @staticmethod
    async def stream_job_events(job_id: str) -> AsyncGenerator[str, None]:
        channel = f"job_channel:{job_id}"
        pubsub = redis_client.pubsub()
        await pubsub.subscribe(channel)

        try:
            # Yield initial snapshot if available
            initial = await redis_client.get(f"job_state:{job_id}")
            if initial:
                yield f"data: {initial}\n\n"
                parsed = json.loads(initial)
                if parsed.get("status") in ("completed", "failed"):
                    return

            while True:
                message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
                if message:
                    data = message["data"]
                    yield f"data: {data}\n\n"
                    parsed = json.loads(data)
                    if parsed.get("status") in ("completed", "failed"):
                        break
                await asyncio.sleep(0.3)
        finally:
            await pubsub.unsubscribe(channel)
