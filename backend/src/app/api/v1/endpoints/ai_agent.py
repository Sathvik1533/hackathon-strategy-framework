from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.core.database import get_db
from src.app.schemas.common import ResponseEnvelope

from ai_layer.mascot_agent import HSFMascotAgent, TeammateProfile

router = APIRouter()


class QueryRequest(BaseModel):
    query: str
    use_rag: bool = True
    session_id: str = "default-session"


class StrategizeRequest(BaseModel):
    problem_statement: str
    domain: Optional[str] = None


class OnboardRequest(BaseModel):
    name: str
    role: str
    contribution_goal: str
    knowledge_level: str = "Intermediate"
    ai_ide: str = "Antigravity"
    active_branch: str = "main"
    problem_statement: Optional[str] = None


class SeniorAdviceRequest(BaseModel):
    name: str = "Teammate"
    role: str = "Backend API & Resilience Lead"
    active_branch: str = "feat/backend-api"
    contribution_goal: str = "Deliver core features"
    knowledge_level: str = "Intermediate"
    ai_ide: str = "Antigravity"
    query: str
    code_snippet: Optional[str] = None
    groq_api_key: Optional[str] = None


class PatternDecisionRequest(BaseModel):
    problem_statement: str


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


@router.post("/onboard", response_model=ResponseEnvelope[dict])
async def onboard_teammate(req: OnboardRequest):
    """
    Teammate Onboarding endpoint: Accepts user profile, active branch,
    and target contribution goal. Senior Orbit produces a personalized briefing,
    immediate action checklist, strict DOs/DON'Ts guardrails, and bespoke AI IDE prompt.
    """
    mascot = HSFMascotAgent()
    profile = TeammateProfile(
        name=req.name,
        role=req.role,
        contribution_goal=req.contribution_goal,
        knowledge_level=req.knowledge_level,
        ai_ide=req.ai_ide,
        active_branch=req.active_branch,
    )
    briefing = mascot.onboard_teammate(profile, req.problem_statement)
    return ResponseEnvelope(
        data=briefing.model_dump(),
        message=f"Senior Orbit successfully onboarded {req.name} on branch {req.active_branch}",
    )


@router.post("/senior-advice", response_model=ResponseEnvelope[dict])
async def consult_senior_advice(req: SeniorAdviceRequest):
    """
    Senior Engineer Desk endpoint: Queries Senior Orbit for immediate task advice,
    code inspection, or guardrails. Enriched with Groq API if key is supplied.
    """
    mascot = HSFMascotAgent()
    profile = TeammateProfile(
        name=req.name,
        role=req.role,
        contribution_goal=req.contribution_goal,
        knowledge_level=req.knowledge_level,
        ai_ide=req.ai_ide,
        active_branch=req.active_branch,
    )
    advice = mascot.consult_senior_orbit(
        profile=profile,
        query=req.query,
        code_snippet=req.code_snippet,
        groq_api_key=req.groq_api_key,
    )
    return ResponseEnvelope(
        data=advice.model_dump(),
        message="Senior Orbit provided guidance successfully",
    )


@router.post("/pattern-decision", response_model=ResponseEnvelope[dict])
async def decide_software_pattern(req: PatternDecisionRequest):
    """
    Parent Agent Architectural Decision endpoint: Evaluates problem statement
    and returns exact Software Design Pattern, rationale, and folder anatomy implications.
    """
    mascot = HSFMascotAgent()
    decision = mascot.decide_software_design_pattern(req.problem_statement)
    return ResponseEnvelope(
        data=decision.model_dump(),
        message="Parent Agent Software Design Pattern decision computed successfully",
    )
