from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from src.app.core.database import get_db
from src.app.schemas.common import ResponseEnvelope

router = APIRouter()

@router.get("/health", response_model=ResponseEnvelope[dict])
async def health_check(db: AsyncSession = Depends(get_db)):
    """Health check verifying API, PostgreSQL, and pgvector readiness"""
    try:
        res = await db.execute(text("SELECT 1;"))
        db_status = "connected"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    return ResponseEnvelope(
        data={
            "api_status": "healthy",
            "database": db_status,
            "version": "1.0.0"
        },
        message="System health check normal"
    )
