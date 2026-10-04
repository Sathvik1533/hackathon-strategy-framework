from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from src.app.schemas.common import ResponseEnvelope
from src.app.schemas.job import JobCreate, JobResponse
from src.app.services.job_service import JobService

router = APIRouter()


@router.post("/render", response_model=ResponseEnvelope[JobResponse])
async def create_background_job(job_in: JobCreate):
    """Enqueues a long-running agent or media transcode job"""
    job_id = await JobService.enqueue_job(job_in.task_type, job_in.payload)
    return ResponseEnvelope(
        data=JobResponse(job_id=job_id, status="queued"),
        message="Background task enqueued successfully",
    )


@router.get("/{job_id}/stream")
async def stream_job_progress(job_id: str):
    """Streams live execution logs to frontend via Server-Sent Events (SSE)"""
    return StreamingResponse(JobService.stream_job_events(job_id), media_type="text/event-stream")
