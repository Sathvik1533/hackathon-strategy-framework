from typing import Any

from pydantic import BaseModel, Field


class JobCreate(BaseModel):
    task_type: str = Field(
        description="Action type, e.g. 'agent_research', 'video_render', 'data_enrich'"
    )
    payload: dict[str, Any] = Field(
        default_factory=dict, description="Job parameters and input context"
    )


class JobResponse(BaseModel):
    job_id: str
    status: str = "queued"
    message: str = "Job successfully enqueued"


class JobProgressEvent(BaseModel):
    status: str
    percent: int
    log: str
    result: dict[str, Any] | None = None
