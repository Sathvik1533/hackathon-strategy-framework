from fastapi import APIRouter
from src.app.api.v1.endpoints import ai_agent, analytics, auth, documents, health, jobs

api_v1_router = APIRouter()

api_v1_router.include_router(health.router, tags=["Health"])
api_v1_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_v1_router.include_router(jobs.router, prefix="/jobs", tags=["Async Jobs & SSE"])
api_v1_router.include_router(ai_agent.router, prefix="/agent", tags=["AI Agent"])
api_v1_router.include_router(
    documents.router, prefix="/documents", tags=["Document Vault & Search"]
)
api_v1_router.include_router(
    analytics.router, prefix="/analytics", tags=["System Telemetry & Analytics"]
)
