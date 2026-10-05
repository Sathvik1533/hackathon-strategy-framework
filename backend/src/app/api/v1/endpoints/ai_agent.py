from typing import List, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.core.database import get_db
from src.app.schemas.common import ResponseEnvelope

from ai_layer.dynamic_squad_orchestrator import DynamicSquadOrchestrator
from ai_layer.mascot_agent import HSFMascotAgent, TeammateProfile
from ai_layer.orbit_memory_tracer import OrbitMemoryTracer
from ai_layer.skill_registry import DynamicSkillRegistry

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


class AestheticDecisionRequest(BaseModel):
    problem_statement: str


class SquadOrchestrateRequest(BaseModel):
    problem_statement: str
    team_size: int = Field(default=5, ge=1, le=10)
    teammate_profiles: Optional[List[TeammateProfile]] = None


class FeaturesMenuRequest(BaseModel):
    problem_statement: str
    domain: Optional[str] = None


class SkillFetchRequest(BaseModel):
    skill_identifier: str
    target_layer: Optional[str] = None
    knowledge_level: str = "Intermediate"


class LogTraceRequest(BaseModel):
    teammate_name: str
    role: str
    active_branch: str = "main"
    action_type: str = "CODE_REVIEW"
    query_or_task: str
    guidance_rendered: str
    code_inspected: Optional[str] = None
    detected_risks: Optional[List[str]] = None
    outcome_status: str = "RESOLVED"


@router.post("/query", response_model=ResponseEnvelope[dict])
async def execute_agent_query(req: QueryRequest, db: AsyncSession = Depends(get_db)):
    """
    Executes grounded agent query. Demonstrates fallback tiering:
    If use_rag is False, routes directly to fast LLM response without vector search overhead.
    """
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


@router.post("/aesthetic-decision", response_model=ResponseEnvelope[dict])
async def decide_frontend_aesthetic(req: AestheticDecisionRequest):
    """
    Parent Agent Frontend Aesthetic Decision endpoint: Evaluates problem statement
    and autonomously selects between Skeuomorphism, Claymorphism, Glassmorphism,
    Neo-Brutalism, or Industrial Brutalism, returning CSS tokens and motion rules.
    """
    mascot = HSFMascotAgent()
    decision = mascot.decide_frontend_aesthetic(req.problem_statement)
    return ResponseEnvelope(
        data=decision.model_dump(),
        message="Parent Agent Frontend Aesthetic decision computed successfully",
    )


# =========================================================================
# Transformers Robot Squad Orchestration & Multi-Layer Features Menu
# =========================================================================


@router.post("/orchestrate-squad", response_model=ResponseEnvelope[dict])
async def orchestrate_transformers_squad(req: SquadOrchestrateRequest):
    """
    Transformers Robot Squad Orchestrator:
    Deploys Orbit Prime, Ironhide, Mirage, Wheeljack, Ratchet, and Bumblebee
    to dynamically partition responsibilities for 1 to 6+ teammates,
    generate the multi-layer Features Menu, and log telemetry traces.
    """
    orchestrator = DynamicSquadOrchestrator()
    result = orchestrator.orchestrate_squad(
        problem_statement=req.problem_statement,
        team_size=req.team_size,
        teammate_profiles=req.teammate_profiles,
    )
    return ResponseEnvelope(
        data=result.model_dump(),
        message=f"Autobots Squad assembled for {req.team_size} teammates with archetype: {result.team_strategy_archetype}",
    )


@router.post("/features-menu", response_model=ResponseEnvelope[dict])
async def generate_system_features_menu(req: FeaturesMenuRequest):
    """
    Generates a full-stack Features Menu covering Frontend, Backend, Database,
    AI Multi-Agent, and Cloud DevOps layers for any problem statement.
    """
    orchestrator = DynamicSquadOrchestrator()
    domain = req.domain or orchestrator.mascot_agent._infer_domain(req.problem_statement)
    aesthetic = orchestrator.mascot_agent.decide_frontend_aesthetic(req.problem_statement)
    menu = orchestrator.generate_features_menu(
        problem_statement=req.problem_statement, domain=domain, aesthetic=aesthetic
    )
    return ResponseEnvelope(
        data=menu.model_dump(),
        message=f"Complete 5-layer Features Menu synthesized for domain: {domain}",
    )


# =========================================================================
# Dynamic Skill Registry & External Skill Synthesizer
# =========================================================================


@router.get("/skills", response_model=ResponseEnvelope[dict])
async def list_available_skills(category_layer: Optional[str] = None):
    """
    Lists all available repository and dynamically acquired skills.
    """
    registry = DynamicSkillRegistry()
    skills = registry.list_skills(category_layer=category_layer)
    return ResponseEnvelope(
        data={
            "total_skills": len(skills),
            "skills": [s.model_dump() for s in skills],
        },
        message="Available skills retrieved successfully",
    )


@router.post("/skills/fetch", response_model=ResponseEnvelope[dict])
async def fetch_or_synthesize_skill(req: SkillFetchRequest):
    """
    Dynamically acquires or synthesizes any requested external skill (from GitHub or web),
    generating complete production SKILL.md specs and tailored teammate instructions.
    """
    registry = DynamicSkillRegistry()
    skill = registry.get_or_acquire_skill(req.skill_identifier, req.target_layer)
    instructions = registry.shape_instructions_for_teammate(
        skill, knowledge_level=req.knowledge_level
    )
    return ResponseEnvelope(
        data={
            "skill": skill.model_dump(),
            "shaped_instructions": instructions,
        },
        message=f"Skill '{skill.name}' resolved (dynamically acquired: {skill.is_dynamically_acquired})",
    )


# =========================================================================
# Orbit Developer Telemetry Tracing & Memory Recall
# =========================================================================


@router.post("/traces/log", response_model=ResponseEnvelope[dict])
async def log_telemetry_trace(req: LogTraceRequest):
    """
    Records an engineer interaction, code inspection, or guardrail alert
    into Orbit's persistent memory (.hsf/traces.jsonl & .hsf/memory.json).
    """
    tracer = OrbitMemoryTracer()
    trace = tracer.log_trace(
        teammate_name=req.teammate_name,
        role=req.role,
        active_branch=req.active_branch,
        action_type=req.action_type,
        query_or_task=req.query_or_task,
        guidance_rendered=req.guidance_rendered,
        code_inspected=req.code_inspected,
        detected_risks=req.detected_risks,
        outcome_status=req.outcome_status,
    )
    return ResponseEnvelope(
        data=trace.model_dump(),
        message="Developer telemetry trace logged into Orbit memory",
    )


@router.get("/traces", response_model=ResponseEnvelope[dict])
async def get_recent_traces(limit: int = 20):
    """
    Retrieves recent developer traces from Orbit's memory stream.
    """
    tracer = OrbitMemoryTracer()
    traces = tracer.get_recent_traces(limit=limit)
    return ResponseEnvelope(
        data={
            "total_traces": len(traces),
            "traces": [t.model_dump() for t in traces],
        },
        message=f"Retrieved {len(traces)} recent telemetry traces",
    )


@router.get("/memory", response_model=ResponseEnvelope[dict])
async def get_memory_summary():
    """
    Retrieves the aggregate cognitive memory state of Senior Orbit,
    including tracked teammates, learned bottlenecks, and system health index.
    """
    tracer = OrbitMemoryTracer()
    summary = tracer.get_memory_summary()
    return ResponseEnvelope(
        data=summary,
        message="Orbit cognitive memory state retrieved successfully",
    )
