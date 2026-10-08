"""
Dynamic Multi-Agent Mentoring Orchestration Engine for HSF.
Orchestrates persona copilots, architecture supervisors, peer synergy agents,
and action dispatchers to mentor teammates end-to-end across all 24-hour hackathon stages.
"""

from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class MentoringStageInfo(BaseModel):
    id: str
    name: str
    hour: str
    objective: str
    milestone_bounty: str
    deliverables: List[str]


class RolePersonaInfo(BaseModel):
    role: str
    autobot: str
    title: str
    superpower: str
    greeting: str


class MentoringConsultationRequest(BaseModel):
    teammate_name: str = Field(..., description="Name of the teammate")
    role: str = Field(..., description="Chosen role, e.g. 'Backend Lead'")
    stage: str = Field(
        default="hour_0",
        description="Current hackathon stage: hour_0, hour_4, hour_12, hour_18, hour_22, hour_24",
    )
    problem_statement: str = Field(
        default="Autonomous Real-Time Agentic Platform", description="Hackathon problem statement"
    )
    current_blocker: Optional[str] = Field(
        default=None, description="Optional current challenge or question"
    )


class MentoringAgentOutput(BaseModel):
    agent_name: str
    role_perspective: str
    advice: str
    action_items: List[str]


class MultiAgentMentoringSession(BaseModel):
    session_id: str
    teammate_name: str
    role: str
    companion: RolePersonaInfo
    current_stage: MentoringStageInfo
    problem_statement: str
    persona_advice: MentoringAgentOutput
    architecture_supervisor: MentoringAgentOutput
    peer_synergy_agent: MentoringAgentOutput
    action_dispatcher: MentoringAgentOutput
    recommended_commands: List[str]
    xp_bounty_available: int
    quest_id: str


HACKATHON_STAGES: Dict[str, MentoringStageInfo] = {
    "hour_0": MentoringStageInfo(
        id="hour_0",
        name="Phase 1: Ideation, Spec & Contracts",
        hour="Hour 0 - 4",
        objective="Deconstruct the problem statement, agree on OpenAPI 3.1 contracts, and establish DDD boundaries.",
        milestone_bounty="Zero-Collision Contract (+200 XP)",
        deliverables=[
            "OpenAPI 3.1 Pydantic v2 data contracts",
            "Supabase Row-Level Security policy schema",
            "Domain-Driven Design bounded contexts",
            "Single-source-of-truth JSON envelope specification",
        ],
    ),
    "hour_4": MentoringStageInfo(
        id="hour_4",
        name="Phase 2: Foundation & Infrastructure Bootstrap",
        hour="Hour 4 - 8",
        objective="Bootstrap full-stack containers, wire Redis 7 connection pool, and establish automated health checks.",
        milestone_bounty="Ignition Sequence (+100 XP)",
        deliverables=[
            "Multi-stage Docker build (<180MB running as non-root)",
            "Redis 7 connection pooling & SETNX distributed locks",
            "FastAPI 0.115+ ResponseEnvelope[T] middleware",
            "Next.js 14 / Orbit Mascot HUD shell live",
        ],
    ),
    "hour_12": MentoringStageInfo(
        id="hour_12",
        name="Phase 3: Neural Core & Feature Velocity",
        hour="Hour 8 - 14",
        objective="Deploy dense HNSW + sparse BM25 hybrid search, FlashRank reranking, and LangGraph multi-agent flow.",
        milestone_bounty="Neural Strike RAG (+250 XP)",
        deliverables=[
            "pgvector 16 cosine similarity (<=>) HNSW index",
            "Reciprocal Rank Fusion (RRF) + FlashRank CPU cross-encoder (<18ms)",
            "LangGraph Cyclic StateGraph with Supervisor routing",
            "FastMCP SSE Tool Sandbox Server running on Port 8001",
        ],
    ),
    "hour_18": MentoringStageInfo(
        id="hour_18",
        name="Phase 4: Distributed Resilience & Fault Recovery",
        hour="Hour 14 - 18",
        objective="Stress-test circuit breakers, enforce rate limits, and verify end-to-end component contracts.",
        milestone_bounty="Resilience Fortress (+300 XP)",
        deliverables=[
            "3-State Circuit Breaker (CLOSED/OPEN/HALF_OPEN) with 30s cooldown",
            "Redis sliding-window IP rate limiting (60 req/min)",
            "Inter-service gRPC / HTTP contract zero-collision check",
            "Automated failover mock testing",
        ],
    ),
    "hour_22": MentoringStageInfo(
        id="hour_22",
        name="Phase 5: Golden Evals & Offline Stage Rehearsal",
        hour="Hour 18 - 22",
        objective="Run 25-case RAGAS golden benchmark, verify 100% test pass, and drill offline stage fail-safe demo.",
        milestone_bounty="Eval Supremacy & Shadow Runner (+750 XP)",
        deliverables=[
            "RAGAS evaluation harness run: Faithfulness >= 0.90",
            "20/20 Pytest unit & integration test assertions passing",
            "pitch/demo.sh tested locally with 0ms internet dependency",
            "Marp pitch deck rendered and timed to 5:30 minutes",
        ],
    ),
    "hour_24": MentoringStageInfo(
        id="hour_24",
        name="Phase 6: Stage Victory & Judge Audit Defense",
        hour="Hour 22 - 24",
        objective="Deliver flawless live stage demonstration and defend technical moats against judge questions.",
        milestone_bounty="Stage Victory Rehearsal (+500 XP)",
        deliverables=[
            "Official System Audit Certification (docs/JUDGE_CERTIFICATION.md)",
            "8 Interactive Archify Blueprints ready to demo",
            "Live Teammate Leaderboard & Quest score presented",
            "Stage fail-safe script armed and ready",
        ],
    ),
}

ROLE_PERSONAS: Dict[str, RolePersonaInfo] = {
    "Lead Architect": RolePersonaInfo(
        role="Lead Architect",
        autobot="Optimus Prime",
        title="Supreme Strategist",
        superpower="Domain boundaries, polyglot coordination, system moats & trade-off clarity",
        greeting="Autobots, transform and roll out! As Lead Architect, your mission is clarity over complexity. We define the boundary and lead the squad to victory.",
    ),
    "Backend Lead": RolePersonaInfo(
        role="Backend Lead",
        autobot="Ironhide",
        title="Resilience Titan",
        superpower="Async gateway throughput, Redis semantic caching, 3-state circuit breakers",
        greeting="Armor locked and canons loaded! I am Ironhide. No upstream outage or timeout will ever crack our backend fortress.",
    ),
    "DevOps Lead": RolePersonaInfo(
        role="DevOps Lead",
        autobot="Bumblebee",
        title="Fleet Commander",
        superpower="Docker multi-stage builds, cloud CI/CD, stage fail-safe offline resilience",
        greeting="Bumblebee on comms! I guarantee 60-second local deploys and zero-latency offline stage demos even if the venue Wi-Fi explodes.",
    ),
    "AI Lead": RolePersonaInfo(
        role="AI Lead",
        autobot="Wheeljack",
        title="Cyber-Scientist",
        superpower="LangGraph cyclic supervisors, FastMCP sandboxes, hybrid RAG & RAGAS evals",
        greeting="Eureka! Wheeljack in the laboratory. We build neural pipelines with zero hallucination and sub-18ms CPU reranking.",
    ),
    "Frontend Lead": RolePersonaInfo(
        role="Frontend Lead",
        autobot="Mirage",
        title="Tactical Strategist",
        superpower="Fluid high-contrast UIs, Senior Orbit Mascot HUD, accessible interactive widgets",
        greeting="Mirage here. The judges judge with their eyes first. We deliver a gorgeous, responsive cyber-cockpit that steals the show.",
    ),
}


class MultiAgentMentorOrchestrator:
    """
    Coordinates dynamic multi-agent mentoring across all 4 specialized subagents:
    1. PersonaMentor (In-character Autobot companion)
    2. ArchitectureSupervisor (System guardrails & risk advisor)
    3. PeerSynergyAgent (Inter-teammate handoff & synchronization)
    4. ActionDispatcher (Immediate executable commands & XP bounties)
    """

    @classmethod
    def get_stages(cls) -> List[MentoringStageInfo]:
        return list(HACKATHON_STAGES.values())

    @classmethod
    def get_roles(cls) -> List[RolePersonaInfo]:
        return list(ROLE_PERSONAS.values())

    @classmethod
    def orchestrate(cls, request: MentoringConsultationRequest) -> MultiAgentMentoringSession:
        stage = HACKATHON_STAGES.get(request.stage, HACKATHON_STAGES["hour_0"])
        persona = ROLE_PERSONAS.get(request.role, ROLE_PERSONAS["Lead Architect"])

        # 1. Persona Mentor Agent Generation
        persona_advice = cls._generate_persona_advice(request, persona, stage)

        # 2. Architecture Supervisor Agent Generation
        arch_advice = cls._generate_architecture_advice(request, persona, stage)

        # 3. Peer Synergy Agent Generation
        synergy_advice = cls._generate_peer_synergy(request, persona, stage)

        # 4. Action Dispatcher Generation
        dispatcher_advice, commands, xp_bounty, quest_id = cls._generate_action_dispatch(
            request, persona, stage
        )

        session_id = f"mentor-{request.teammate_name.lower().replace(' ', '-')}-{stage.id}"

        return MultiAgentMentoringSession(
            session_id=session_id,
            teammate_name=request.teammate_name,
            role=request.role,
            companion=persona,
            current_stage=stage,
            problem_statement=request.problem_statement,
            persona_advice=persona_advice,
            architecture_supervisor=arch_advice,
            peer_synergy_agent=synergy_advice,
            action_dispatcher=dispatcher_advice,
            recommended_commands=commands,
            xp_bounty_available=xp_bounty,
            quest_id=quest_id,
        )

    @classmethod
    def _generate_persona_advice(
        cls, req: MentoringConsultationRequest, persona: RolePersonaInfo, stage: MentoringStageInfo
    ) -> MentoringAgentOutput:
        blocker_text = (
            f" Addressing your blocker '{req.current_blocker}'." if req.current_blocker else ""
        )

        advice_templates = {
            "hour_0": f"Greetings {req.teammate_name}! We are tackling '{req.problem_statement}'.{blocker_text} In this first hour, resist writing premature business logic. Lock down the OpenAPI contract and schema models first. If contracts are airtight, frontend and backend can build simultaneously with zero blocking.",
            "hour_4": f"Keep moving, {req.teammate_name}! Time to establish our infrastructure skeleton.{blocker_text} Run './init.sh' and ensure our Docker containers spin up cleanly. Test Redis connectivity with 'curl http://localhost:8000/api/v1/health' to confirm the heartbeat.",
            "hour_12": f"Now we unleash our technical core! For '{req.problem_statement}', judges want to see true intelligence, not static mocks.{blocker_text} Implement hybrid search with pgvector 16 and FlashRank CPU reranking. Verify our LangGraph supervisor loops cleanly through tools.",
            "hour_18": f"Resilience time! When judges test our app, will it crash if an external API lags? Never on our watch.{blocker_text} Verify our 3-state Circuit Breaker. Force a mock failure and show judges the automated 30s cooldown and local cached fallback.",
            "hour_22": f"Golden milestone, {req.teammate_name}! We must prove zero hallucination with data.{blocker_text} Run our RAGAS evaluation harness across our 25-case test suite. Practice the 30-second stage demo script using 'bash pitch/demo.sh'.",
            "hour_24": f"Victory is within reach! All 8 Archify architecture blueprints are certified and our teammate leaderboard is live.{blocker_text} Deliver the pitch with confidence. Hand judges the audit certificate at 'docs/JUDGE_CERTIFICATION.md'.",
        }

        action_templates = {
            "hour_0": [
                f"Define schema models for '{req.problem_statement}' in src/app/schemas/",
                "Verify single-source-of-truth ResponseEnvelope[T] envelope format",
                "Review Supabase Row-Level Security policies in database/supabase_rls.sql",
            ],
            "hour_4": [
                "Run './init.sh' to verify Docker Compose and Redis 7 health",
                "Execute 'npx hsf wizard' to refresh your role environment",
                "Verify API health endpoint responds in <50ms",
            ],
            "hour_12": [
                "Seed pgvector 16 with domain vectors using python3 database/seed_data.py",
                "Test FlashRank cross-encoder latency (<18ms target)",
                "Verify LangGraph supervisor routes through human_gate",
            ],
            "hour_18": [
                "Trigger circuit breaker test to confirm OPEN state trip after 3 failures",
                "Verify Redis semantic cache hits (<8ms P95 latency)",
                "Run 'ruff check .' to guarantee zero lint warnings",
            ],
            "hour_22": [
                "Run full test suite: PYTHONPATH=backend pytest (expect 20/20 passing)",
                "Execute offline fail-safe: bash pitch/demo.sh",
                "Verify Marp pitch presentation deck: pitch/pitch.marp.md",
            ],
            "hour_24": [
                "Compile judge certification report: python3 scripts/generate_judge_report.py",
                "Open Archify blueprints gallery: open docs/architecture/index.html",
                "Inspect live scoreboard: npx hsf leaderboard",
            ],
        }

        return MentoringAgentOutput(
            agent_name=f"{persona.autobot} ({persona.title})",
            role_perspective=f"Primary Companion for {req.role}",
            advice=advice_templates.get(stage.id, advice_templates["hour_0"]),
            action_items=action_templates.get(stage.id, action_templates["hour_0"]),
        )

    @classmethod
    def _generate_architecture_advice(
        cls, req: MentoringConsultationRequest, persona: RolePersonaInfo, stage: MentoringStageInfo
    ) -> MentoringAgentOutput:
        return MentoringAgentOutput(
            agent_name="Architect Supervisor Sentinel",
            role_perspective="System Design & Risk Governance",
            advice=f"Guardrail Check for {stage.name}: Ensure we avoid hackathon anti-patterns. Never hardcode mocks in backend routes; use Redis semantic caching with deterministic fallbacks. Maintain zero-collision boundaries between Python AI services and any external enterprise components.",
            action_items=[
                "Enforce ResponseEnvelope[T] across all API responses",
                "Verify parameterized SQL queries to prevent injection",
                "Ensure non-root appuser UID 10001 in Docker multi-stage configuration",
            ],
        )

    @classmethod
    def _generate_peer_synergy(
        cls, req: MentoringConsultationRequest, persona: RolePersonaInfo, stage: MentoringStageInfo
    ) -> MentoringAgentOutput:
        synergy_map = {
            "Lead Architect": "Synchronize with Backend Lead on schema schemas and Frontend Lead on UI wireframes. Ensure DevOps Lead has environment secrets verified.",
            "Backend Lead": "Hand off OpenAPI 3.1 endpoints to Frontend Lead so UI can mock and bind immediately. Coordinate with AI Lead on FastMCP tool schemas.",
            "Frontend Lead": "Pull OpenAPI types from backend router. Embed Senior Orbit Mascot HUD into dashboard. Keep DevOps Lead informed of build assets.",
            "DevOps Lead": "Notify team once Docker stack and Redis are healthy. Ensure offline demo runner (pitch/demo.sh) is accessible to the speaker.",
            "AI Lead": "Deliver vector search endpoint to Backend Lead. Confirm with Architect that human-in-the-loop gate is registered before dangerous tools.",
        }
        return MentoringAgentOutput(
            agent_name="Peer Synergy Coordinator",
            role_perspective="Cross-Teammate Synchronization",
            advice=f"Cross-Functional Handoff: {synergy_map.get(req.role, 'Maintain active communication with all teammates.')} Remember to send high-fives via 'npx hsf cheer <teammate>' to boost team XP!",
            action_items=[
                "Share current progress on team channel",
                "Cheer a teammate to award +25 synergy XP",
                "Confirm no uncommitted blockers in git working tree",
            ],
        )

    @classmethod
    def _generate_action_dispatch(
        cls, req: MentoringConsultationRequest, persona: RolePersonaInfo, stage: MentoringStageInfo
    ):
        cmd_map = {
            "hour_0": [
                "npx hsf wizard",
                "curl http://localhost:8000/docs",
                "npx hsf diagram polyglot",
            ],
            "hour_4": [
                "./init.sh",
                "curl http://localhost:8000/api/v1/health",
                "npx hsf diagram topology",
            ],
            "hour_12": [
                "python3 database/seed_data.py",
                "curl http://localhost:8001/sse",
                "npx hsf diagram dataflow",
            ],
            "hour_18": [
                "curl http://localhost:8000/api/v1/health/circuit-breakers",
                "ruff check .",
                "npx hsf diagram lifecycle",
            ],
            "hour_22": ["PYTHONPATH=backend pytest", "bash pitch/demo.sh", "npx hsf diagram all"],
            "hour_24": [
                "npx hsf leaderboard",
                "python3 scripts/generate_judge_report.py",
                "open docs/architecture/index.html",
            ],
        }
        xp_map = {
            "hour_0": 200,
            "hour_4": 100,
            "hour_12": 250,
            "hour_18": 300,
            "hour_22": 750,
            "hour_24": 500,
        }
        quest_map = {
            "hour_0": "q-contract",
            "hour_4": "q-ignition",
            "hour_12": "q-neural-strike",
            "hour_18": "q-resilience-fortress",
            "hour_22": "q-eval-supremacy",
            "hour_24": "q-stage-victory",
        }

        commands = cmd_map.get(stage.id, ["npx hsf wizard"])
        xp = xp_map.get(stage.id, 150)
        qid = quest_map.get(stage.id, "q-autobot")

        output = MentoringAgentOutput(
            agent_name="Action Item Dispatcher",
            role_perspective="Executable Tasks & Gamification Bounty",
            advice=f"Next immediate milestone: Complete stage deliverables to claim bounty '{stage.milestone_bounty}'. Run the recommended commands below.",
            action_items=[f"Execute: {cmd}" for cmd in commands]
            + [
                f"Claim bounty upon completion: npx hsf quest claim {qid} --teammate '{req.teammate_name}'"
            ],
        )

        return output, commands, xp, qid
