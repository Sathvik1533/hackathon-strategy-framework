from typing import Any

from pydantic import BaseModel, Field


class DocumentChunkCreate(BaseModel):
    title: str = Field(..., max_length=255, description="Document or section title")
    content: str = Field(..., description="Raw text content of the chunk")
    source: str = Field(
        "manual", max_length=255, description="Source provenance (e.g., pdf, web, manual)"
    )
    embedding: list[float] | None = Field(
        None, description="Optional pre-computed 1536-dim embedding vector"
    )


class DocumentChunkResponse(BaseModel):
    id: int
    title: str | None = None
    content: str
    source: str | None = "manual"
    created_at: Any | None = None


class DocumentSearchRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Search query string")
    top_k: int = Field(5, ge=1, le=50, description="Number of results to return")
    use_rerank: bool = Field(True, description="Whether to apply neural cross-encoder reranking")


class DocumentSearchResult(BaseModel):
    id: int
    title: str | None = None
    content: str
    source: str | None = None
    score: float
    rank: int
