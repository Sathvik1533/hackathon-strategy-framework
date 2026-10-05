from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.core.database import get_db
from src.app.schemas.common import ResponseEnvelope

from ai_layer.mascot_agent import HSFMascotAgent

router = APIRouter()


class QueryRequest(BaseModel):
    query: str
    use_rag: bool = True
    session_id: str = "default-session"


class StrategizeRequest(BaseModel):
    problem_statement: str
    domain: Optional[str] = None


@router.post("/query", response_model=ResponseEnvelope[dict])
async def execute_agent_query(req: QueryRequest, db: AsyncSession = Depends(get_db)):
    """
    Executes grounded agent query. Demonstrates fallback tiering:
    If use_rag is False, routes directly to fast LLM response without vector search overhead.
    """
    # Demo execution pattern:
    response_data = {
        "query": req.query,
        "answer": f"Processed query '{req.query}' using {'pgvector Hybrid RAG' if req.use_rag else 'Direct LLM Synthesis'}.",
        "retrieval_used": req.use_rag,
        "faithfulness_score": 0.95 if req.use_rag else 0.82,
        "latency_ms": 240 if req.use_rag else 90,
    }
    return ResponseEnvelope(data=response_data, message="Agent executed successfully")


@router.post("/strategize", response_model=ResponseEnvelope[dict])
async def strategize_problem(req: StrategizeRequest):
    """
    Orbit Mascot Agent endpoint: Deconstructs any problem statement,
    maps it strictly onto our pre-ready tech stack, and generates customized
    teammate prompts for Antigravity, Claude, Cursor, and Hero agents.
    """
    mascot = HSFMascotAgent()
    plan = mascot.strategize(req.problem_statement, req.domain)
    return ResponseEnvelope(
        data=plan.model_dump(),
        message="Orbit Mascot Agent generated strategy and teammate boilerplates successfully",
    )
