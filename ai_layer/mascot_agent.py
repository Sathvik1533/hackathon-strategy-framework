"""
Orbit: The Hackathon Strategy Mascot & Autonomous Problem Decomposer
(ai_layer/mascot_agent.py)

Autonomous internal agent that ingests any hackathon problem statement,
deconstructs requirements, maps them strictly onto our pre-ready tech stack,
selects the exact tools and skills to activate, provides competitive moat analysis,
and generates ready-made boilerplate prompts for Antigravity, Claude, Cursor, and Hero agents.
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from typing import Dict, List, Optional

from pydantic import BaseModel


class TeammatePromptBoilerplate(BaseModel):
    role_title: str
    target_layer: str
    assigned_skills: List[str]
    core_files: List[str]
    custom_agent_prompt: str


class TechStackMapping(BaseModel):
    fastapi_endpoints: List[str]
    database_tables: List[str]
    vector_embedding_dimension: int = 1536
    vector_search_type: str = "HNSW Cosine (<=>) + TSVECTOR BM25 Hybrid (RRF)"
    redis_keys: List[str]
    langgraph_nodes: List[str]
    human_approval_gate_step: str
    fastmcp_tools: List[str]
    flashrank_top_k: int = 5
    supabase_rls_policy: str
    aws_fargate_task: str


class SoftwareDesignPatternDecision(BaseModel):
    pattern_name: str
    architectural_style: str
    design_patterns_applied: List[str]
    why_chosen: str
    why_not_microservices: str
    why_not_simple_monolith: str
    folder_anatomy_implications: Dict[str, str]
    recommended_team_delegation: Dict[str, str]


class SeniorEngineerGuidance(BaseModel):
    senior_engineer_name: str = "Senior Orbit 👓🤖"
    role: str
    active_branch: str
    current_mission: str
    immediate_actions_what_to_do: List[str]
    critical_guardrails_what_not_to_do: List[str]
    code_review_rules: List[str]
    recommended_files: List[str]
    forbidden_antipatterns: List[str]
    senior_pro_tip: str


class TeammateProfile(BaseModel):
    name: str
    role: str
    contribution_goal: str
    knowledge_level: str = "Intermediate"  # Beginner, Intermediate, Advanced, Senior
    ai_ide: str = "Antigravity"  # Antigravity, Claude, Cursor, Windsurf, Hero Agent
    active_branch: str = "main"


class OnboardingBriefing(BaseModel):
    profile: TeammateProfile
    welcome_message: str
    personalized_mission: str
    design_pattern_summary: SoftwareDesignPatternDecision
    senior_guidance: SeniorEngineerGuidance
    customized_ai_ide_prompt: str
    suggested_git_commands: List[str]


class SeniorAdviceResponse(BaseModel):
    senior_engineer_name: str = "Senior Orbit 👓🤖"
    query: str
    active_branch: str
    advice: str
    what_to_do: List[str]
    what_not_to_do: List[str]
    code_critique: Optional[str] = None
    groq_powered: bool = False


class MascotStrategyPlan(BaseModel):
    mascot_name: str = "Orbit 🤖🚀"
    problem_statement: str
    domain_classified: str
    executive_strategy: str
    competitive_advantage_vs_peers: List[str]
    skills_activated: List[str]
    tech_stack_mapping: TechStackMapping
    software_design_pattern: Optional[SoftwareDesignPatternDecision] = None
    teammate_prompts: Dict[str, TeammatePromptBoilerplate]
    stage_pitch_hook: str
    estimated_setup_time_minutes: int = 1


class HSFMascotAgent:
    """
    Orbit: The internal mascot and strategy director for HSF.
    Deconstructs problem statements and generates actionable boilerplates
    and agent prompts aligned exclusively with our production stack.
    """

    def __init__(self, name: str = "Orbit 🤖🚀"):
        self.name = name

    def _infer_domain(self, problem: str) -> str:
        p_lower = problem.lower()
        if any(w in p_lower for w in ["health", "medic", "patient", "clinic", "bio", "pharma"]):
            return "Healthcare & Life Sciences"
        elif any(
            w in p_lower
            for w in ["fintech", "fraud", "bank", "pay", "money", "loan", "trade", "crypto"]
        ):
            return "Financial Technology & Risk Intelligence"
        elif any(w in p_lower for w in ["edu", "learn", "tutor", "school", "teach", "student"]):
            return "Education & Adaptive Learning"
        elif any(w in p_lower for w in ["supply", "chain", "logist", "cargo", "ship", "warehous"]):
            return "Supply Chain & Autonomous Logistics"
        elif any(w in p_lower for w in ["legal", "contract", "compliance", "law", "audit"]):
            return "LegalTech & Regulatory Compliance"
        elif any(w in p_lower for w in ["cyber", "secur", "vulnerab", "threat", "hack"]):
            return "Cybersecurity & Autonomous Threat Defense"
        elif any(w in p_lower for w in ["climate", "energy", "carbon", "sustain", "green"]):
            return "CleanTech & Renewable Energy Intelligence"
        return "Autonomous Enterprise Intelligence"

    def strategize(
        self, problem_statement: str, domain: Optional[str] = None
    ) -> MascotStrategyPlan:
        """
        Decomposes the problem statement and crafts a comprehensive strategy plan
        utilizing our pre-ready stack, pre-installed skills, and 5-person squad prompts.
        """
        cleaned_problem = problem_statement.strip()
        detected_domain = domain or self._infer_domain(cleaned_problem)
        slug = re.sub(r"[^a-zA-Z0-9]+", "_", detected_domain.lower()).strip("_")

        # 1. Tech Stack Mapping (Strictly using our stack)
        tech_mapping = TechStackMapping(
            fastapi_endpoints=[
                "/api/v1/health (Liveness & vector extension probe)",
                f"/api/v1/{slug}/ingest (Multipart upload with chunking & pgvector embeddings)",
                f"/api/v1/{slug}/jobs/render (Asynchronous workflow dispatcher enqueued to Redis)",
                f"/api/v1/{slug}/jobs/{{id}}/stream (Real-time SSE token & progress log channel)",
                f"/api/v1/{slug}/query (Hybrid pgvector RRF retrieval + FlashRank reranker)",
                "/api/v1/analytics/telemetry (P95 latency, circuit breaker state, RAGAS metrics)",
            ],
            database_tables=[
                f"{slug}_documents (id UUID, title VARCHAR, meta JSONB, created_at TIMESTAMPTZ)",
                f"{slug}_chunks (id UUID, doc_id UUID REFERENCES, content TEXT, embedding vector(1536), tsv_content TSVECTOR)",
                f"{slug}_audit_trail (id UUID, user_id UUID, action VARCHAR, details JSONB, approved_by VARCHAR)",
            ],
            vector_embedding_dimension=1536,
            vector_search_type="HNSW Cosine (<=>) + TSVECTOR BM25 Hybrid (RRF k=60)",
            redis_keys=[
                f"cache:semantic:{slug}:<sha256> (Sub-10ms repeat query responses)",
                "channel:jobs:<uuid> (Real-time SSE Pub/Sub telemetry broadcast)",
                "state:jobs:<uuid> (Job progress snapshot for reconnecting browsers)",
                f"lock:idempotency:{slug}:<key> (Distributed SETNX mutex lock, TTL 120s)",
                "ratelimit:<ip>:<window> (Sliding-window token budget counter)",
            ],
            langgraph_nodes=[
                "DomainParserNode (Sanitizes input, routes query via Jev System-1)",
                "HybridRetrieverNode (Dense pgvector + Sparse BM25 Reciprocal Rank Fusion)",
                "FlashRankNeuralRerankerNode (Reranks candidates to top 5 in <20ms)",
                "SpecialistWorkerNode (Synthesizes domain answer with strict Pydantic schemas)",
                "HumanApprovalGateNode (Interrupts before final state commit for sensitive operations)",
            ],
            human_approval_gate_step="interrupt_before=['human_gate'] prior to executing irreversible database writes or external actions",
            fastmcp_tools=[
                f"{slug}_fetch_evidence (Fetches external verification records via SSE)",
                f"{slug}_verify_compliance (Runs isolated compliance checks in port 8001 sandbox)",
            ],
            flashrank_top_k=5,
            supabase_rls_policy=f"ALTER TABLE {slug}_chunks ENABLE ROW LEVEL SECURITY; CREATE POLICY tenant_isolation ON {slug}_chunks FOR ALL USING (auth.uid() = user_id);",
            aws_fargate_task="infra/aws-ecs-task-definition.json (0.5 vCPU, 1024MB RAM, Port 8000 target group)",
        )

        # 2. Competitive Advantage vs Peer Competitors
        competitive_moats = [
            "⚡ 14-Hour Head Start: While peer competitors struggle with Docker, CORS, and vector extensions, our entire stack is live in 60s.",
            "🛡️ Zero 'AI Slop' Deductions: Monolithic prompts hallucinate; our LangGraph cyclic supervisor with RAGAS benchmarks mathematically proves >0.90 faithfulness.",
            "🔒 Bank-Grade Multi-Tenant Isolation: Competitors write raw SQL; our Supabase Row-Level Security (auth.uid()) guarantees zero cross-tenant leaks.",
            "⚡ Sub-10ms Demonstration Speed: Competitors wait 6s per LLM generation; our Redis semantic cache returns stored answers in <10ms on repeat demo queries.",
            "📶 Wi-Fi Drop Immunity on Stage: If venue Wi-Fi freezes, competitors panic; our 3-state Circuit Breaker, Marp offline deck, and cURL terminal demo (demo.sh) ensure a 100% flawless presentation.",
        ]

        # 3. Skills Activated in Chronological Order
        skills_activated = [
            "hackathon-speedrun-kit",
            "poetry-python-packaging",
            "context7-docs-fetcher",
            "archify",
            "hallmark",
            "emil-design-eng",
            "fastapi-production-archetype",
            "async-agent-celery-redis",
            "pgvector-hybrid-search",
            "supabase-rls",
            "langgraph-production-patterns",
            "pydantic-ai-workflows",
            "fastmcp-tool-server",
            "jev-decision-router",
            "rag-reranking-pipeline",
            "llm-gateway-semantic-cache",
            "agent-security-guardrails",
            "agent-eval-harness",
            "agent-docker-aws-deploy",
            "marp-presentation-engine",
        ]

        # 4. Tailored Teammate Prompts (Antigravity / Claude / Cursor / Hero Agent Ready)
        prompts = {
            "teammate_1_backend": TeammatePromptBoilerplate(
                role_title="Teammate 1: Backend API & Resilience Lead",
                target_layer="Backend API & Transport Layer",
                assigned_skills=[
                    "fastapi-production-archetype",
                    "async-agent-celery-redis",
                    "context7-docs-fetcher",
                ],
                core_files=[
                    "backend/src/app/api/v1/endpoints/jobs.py",
                    "backend/src/app/core/resilience.py",
                    "backend/src/app/core/redis.py",
                ],
                custom_agent_prompt=(
                    f"You are the Backend API & Resilience Lead for our project: '{cleaned_problem}'.\n"
                    f"Domain: {detected_domain}.\n"
                    f"Your Task:\n"
                    f"1. Implement async FastAPI routes in `backend/src/app/api/v1/endpoints/`:\n"
                    f"   - POST /api/v1/{slug}/jobs/render (Enqueues domain workflow with Redis SETNX idempotency)\n"
                    f"   - GET /api/v1/{slug}/jobs/{{id}}/stream (Streams live progress logs over SSE text/event-stream)\n"
                    f"2. Decorate downstream calls with @retry_with_exponential_backoff and CircuitBreaker.\n"
                    f"3. Ensure all responses strictly use ResponseEnvelope[T]. Run `ruff check . && pytest` before pushing."
                ),
            ),
            "teammate_2_database": TeammatePromptBoilerplate(
                role_title="Teammate 2: Database & Vector Search Lead",
                target_layer="Database & Storage Layer",
                assigned_skills=["pgvector-hybrid-search", "hackathon-speedrun-kit"],
                core_files=[
                    "database/supabase_rls.sql",
                    f"backend/src/app/models/{slug}.py",
                    "database/seed_data.py",
                ],
                custom_agent_prompt=(
                    f"You are the Database & Vector Search Lead for our project: '{cleaned_problem}'.\n"
                    f"Domain: {detected_domain}.\n"
                    f"Your Task:\n"
                    f"1. Define PostgreSQL 16 SQLAlchemy 2.0 async models for `{slug}_documents` and `{slug}_chunks`.\n"
                    f"2. Add 1536-dim HNSW Cosine Index (`<=>`) and GIN TSVECTOR for hybrid search.\n"
                    f"3. Author Supabase Row-Level Security (RLS) policies isolating user records by `auth.uid()` in `database/supabase_rls.sql`.\n"
                    f"4. Customize `database/seed_data.py` to seed 50 realistic {detected_domain} records with synthetic embeddings in 3 seconds."
                ),
            ),
            "teammate_3_ai_agent": TeammatePromptBoilerplate(
                role_title="Teammate 3: AI & Multi-Agent Architecture Lead",
                target_layer="AI & Agentic Layer",
                assigned_skills=[
                    "langgraph-production-patterns",
                    "pydantic-ai-workflows",
                    "fastmcp-tool-server",
                    "rag-reranking-pipeline",
                    "agent-eval-harness",
                ],
                core_files=[
                    "ai_layer/langgraph_supervisor.py",
                    "ai_layer/fastmcp_server.py",
                    "ai_layer/eval_harness.py",
                ],
                custom_agent_prompt=(
                    f"You are the AI & Multi-Agent Lead for our project: '{cleaned_problem}'.\n"
                    f"Domain: {detected_domain}.\n"
                    f"Your Task:\n"
                    f"1. Build a LangGraph cyclic state machine in `ai_layer/langgraph_supervisor.py` with PostgreSQL checkpoint persistence.\n"
                    f"2. Add nodes: DomainParserNode, HybridRetrieverNode (RRF k=60), FlashRankNeuralRerankerNode (<20ms), and WorkerNode.\n"
                    f"3. Configure `interrupt_before=['human_gate']` for human approval before committing high-stakes actions.\n"
                    f"4. Register sandboxed tools in `ai_layer/fastmcp_server.py` over SSE (port 8001).\n"
                    f"5. Run `ai_layer/eval_harness.py` to record RAGAS Faithfulness scores >0.90 for our presentation slides."
                ),
            ),
            "teammate_4_frontend": TeammatePromptBoilerplate(
                role_title="Teammate 4: Frontend Console & Real-Time UX Lead",
                target_layer="Frontend Console & UX Layer",
                assigned_skills=[
                    "hallmark",
                    "emil-design-eng",
                    "awesome-design-systems",
                    "archify",
                ],
                core_files=[
                    "frontend/index.html",
                    "frontend/connectivity.html",
                    "frontend/style.css",
                    "frontend/app.js",
                ],
                custom_agent_prompt=(
                    f"You are the Frontend Console & Real-Time UX Lead for our project: '{cleaned_problem}'.\n"
                    f"Domain: {detected_domain}.\n"
                    f"Your Task:\n"
                    f"1. Customize `frontend/index.html` with high-density dark-mode cards tailored to {detected_domain}.\n"
                    f"2. Wire the EventSource SSE listener to stream live agent logs into the terminal with auto-scrolling and status badges.\n"
                    f"3. Verify that `frontend/connectivity.html` renders all 7 active connection status chips using `connectivity-topology-manager.js`.\n"
                    f"4. Add a prominent button launching our interactive Archify architecture explorer (`docs/architecture/system-architecture.html`)."
                ),
            ),
            "teammate_5_devops_pitch": TeammatePromptBoilerplate(
                role_title="Teammate 5: Cloud DevOps, CI/CD & Pitch / Demo Lead",
                target_layer="DevOps, Cloud & Presentation Layer",
                assigned_skills=[
                    "agent-docker-aws-deploy",
                    "marp-presentation-engine",
                    "hackathon-speedrun-kit",
                ],
                core_files=[
                    "infra/Dockerfile",
                    "pitch/pitch.marp.md",
                    "pitch/demo.sh",
                    "infra/deploy_aws.sh",
                ],
                custom_agent_prompt=(
                    f"You are the Cloud DevOps & Pitch Lead for our project: '{cleaned_problem}'.\n"
                    f"Domain: {detected_domain}.\n"
                    f"Your Task:\n"
                    f"1. Validate our multi-stage Docker build (<180MB non-root appuser) and AWS ECS Fargate task definition.\n"
                    f"2. Tailor our pitch presentation in `pitch/pitch.marp.md` with problem narrative, Archify diagram, RAGAS scores, and business ROI.\n"
                    f"3. Run `npm run pitch` to compile interactive HTML and PDF slides.\n"
                    f"4. Test the emergency live stage fail-safe runner `bash pitch/demo.sh` to ensure a 100% foolproof backup."
                ),
            ),
        }

        stage_hook = (
            f"Every day in {detected_domain}, teams lose hundreds of hours to fragmented data and unverified AI hallucinations. "
            f"Today, our team built the first production-grade autonomous solution with mathematical faithfulness, human safety gates, "
            f"and sub-10ms response times—running on enterprise infrastructure."
        )

        pattern_decision = self.decide_software_design_pattern(cleaned_problem)

        return MascotStrategyPlan(
            mascot_name=self.name,
            problem_statement=cleaned_problem,
            domain_classified=detected_domain,
            executive_strategy=(
                f"Orbit has analyzed '{cleaned_problem}'! We will conquer this domain by mapping its data flows "
                f"directly into our 7-layer HSF architecture under the '{pattern_decision.pattern_name}' pattern. We will leverage PostgreSQL pgvector for hybrid retrieval, "
                f"LangGraph for multi-agent reasoning with a human-in-the-loop safety gate, Redis for sub-10ms semantic caching, "
                f"and present an interactive Archify blueprint backed by verified RAGAS faithfulness metrics."
            ),
            competitive_advantage_vs_peers=competitive_moats,
            skills_activated=skills_activated,
            tech_stack_mapping=tech_mapping,
            software_design_pattern=pattern_decision,
            teammate_prompts=prompts,
            stage_pitch_hook=stage_hook,
            estimated_setup_time_minutes=1,
        )

    def decide_software_design_pattern(
        self, problem_statement: str
    ) -> SoftwareDesignPatternDecision:
        """
        Parent Agent Decision Engine: Evaluates the problem statement and determines
        the exact software design pattern, architectural style, and folder implications
        under 24-hour hackathon constraints.
        """
        p_lower = problem_statement.lower()

        if any(
            w in p_lower
            for w in [
                "iot",
                "telemetry",
                "drone",
                "fraud",
                "stream",
                "sensor",
                "fleet",
                "realtime",
                "event",
                "traffic",
            ]
        ):
            return SoftwareDesignPatternDecision(
                pattern_name="Event-Driven Architecture (EDA) with Asynchronous Redis Streams & CQRS Light",
                architectural_style="Decoupled Event-Driven Pipeline + Asynchronous Worker Mesh",
                design_patterns_applied=[
                    "CQRS Light (Command/Query Responsibility Segregation)",
                    "Publisher-Subscriber Event Bus (Redis Pub/Sub & Streams)",
                    "Distributed Idempotency Mutex (Redis SETNX)",
                    "Observer Pattern over Server-Sent Events (SSE)",
                ],
                why_chosen=(
                    "High-ingestion event streams and telemetry require immediate sub-5ms command acknowledgment "
                    "without blocking read query threads. Decoupling command writes via Redis queues ensures that "
                    "abrupt bursts in sensor signals or transaction spikes never degrade browser dashboard responsiveness."
                ),
                why_not_microservices=(
                    "Pure microservices introduce distributed network latency, cross-service auth token exchanges, "
                    "Docker Compose network routing headaches, and distributed tracing complexity that reliably derails "
                    "teams in a 24-hour sprint. A modular event-bus in a single codebase provides the same decoupling benefits with zero deployment overhead."
                ),
                why_not_simple_monolith=(
                    "A naive monolithic request/response loop blocks the single-threaded asyncio event loop during prolonged "
                    "LLM or embedding calls, resulting in HTTP 504 Gateway Timeouts on stage."
                ),
                folder_anatomy_implications={
                    "backend/src/app/api/v1/": "Thin asynchronous command ingestion and query endpoints.",
                    "backend/src/app/services/": "Domain command handlers publishing events to Redis channels.",
                    "backend/src/app/core/redis.py": "Connection pools for pub/sub event broadcasting.",
                    "ai_layer/": "Background event-consumer workers processing tasks asynchronously.",
                    "frontend/": "EventSource listeners subscribing to real-time SSE event channels.",
                },
                recommended_team_delegation={
                    "Backend Lead": "Build command endpoints, validate inputs, publish events to Redis.",
                    "Database Lead": "Append-only event tables and pgvector HNSW indexing.",
                    "AI Lead": "Asynchronous event-consumer workers with LangGraph state.",
                    "Frontend Lead": "High-density real-time telemetry stream UI.",
                    "DevOps Lead": "Redis cluster configuration and minimal Docker deployment.",
                },
            )

        elif any(
            w in p_lower
            for w in [
                "agent",
                "tool",
                "mcp",
                "doctor",
                "health",
                "clinical",
                "legal",
                "audit",
                "compliance",
                "multi-agent",
            ]
        ):
            return SoftwareDesignPatternDecision(
                pattern_name="Modular Monolith with Hexagonal Ports & Adapters + FastMCP Tool Isolation",
                architectural_style="Hexagonal Architecture (Clean Architecture / Ports & Adapters)",
                design_patterns_applied=[
                    "Ports & Adapters (Hexagonal Architecture)",
                    "Supervisor-Worker Multi-Agent Pattern (LangGraph)",
                    "Human-in-the-Loop Interrupt Gate Pattern",
                    "Repository Pattern with Row-Level Security",
                ],
                why_chosen=(
                    "Complex multi-agent reasoning and sensitive domain rules require strict isolation between "
                    "core business rules, external LLM model providers, and third-party tools. If an external tool or "
                    "scraper crashes, the isolated adapter catches the fault without corrupting system state."
                ),
                why_not_microservices=(
                    "Splitting every agent and tool into independent container services creates massive version drift, "
                    "uncoordinated database migrations, and complex deployment pipelines that burn valuable hackathon hours."
                ),
                why_not_simple_monolith=(
                    "Tightly coupling LLM prompts with direct database queries creates brittle spaghetti code where "
                    "changing a database column breaks agent reasoning nodes."
                ),
                folder_anatomy_implications={
                    "backend/src/app/core/": "Invariant domain ports (resilience, database session protocols).",
                    "ai_layer/fastmcp_server.py": "Outbound tool adapter running on isolated port 8001.",
                    "ai_layer/langgraph_supervisor.py": "Core agent state supervisor and orchestrator node.",
                    "database/supabase_rls.sql": "Persistence adapter enforcing multi-tenant isolation.",
                },
                recommended_team_delegation={
                    "Backend Lead": "Inbound REST ports and Pydantic validation adapters.",
                    "Database Lead": "Postgres repository layer and Supabase RLS security policies.",
                    "AI Lead": "Supervisor state machine and FastMCP tool adapters.",
                    "Frontend Lead": "Agent execution console and live terminal trace viewer.",
                    "DevOps Lead": "Multi-stage Docker build and AWS ALB health probes.",
                },
            )

        else:
            return SoftwareDesignPatternDecision(
                pattern_name="Modular Monolith with Event-Driven Background Workers (Redis Pub/Sub)",
                architectural_style="Production-Grade Modular Monolith + Async Worker Mesh",
                design_patterns_applied=[
                    "Modular Monolith (Package by Feature / Layer)",
                    "Producer-Consumer Asynchronous Pipeline",
                    "Reciprocal Rank Fusion (RRF) Hybrid Search",
                    "Resilience Decorators (Circuit Breaker + Exponential Backoff)",
                ],
                why_chosen=(
                    "The undisputed gold standard for 24-hour hackathon execution. Combines the rapid development velocity "
                    "and instantaneous debugging of a single repository with the resilience of decoupled async background workers."
                ),
                why_not_microservices=(
                    "Microservices are an infamous hackathon trap. Teams spend 14 hours debugging cross-container CORS, "
                    "networking, and distributed database migrations, presenting a broken demo. A modular monolith wins on velocity and reliability."
                ),
                why_not_simple_monolith=(
                    "Single-file monolithic scripts fail under concurrent user load and cannot stream real-time tokens to the browser."
                ),
                folder_anatomy_implications={
                    "frontend/": "High-density vanilla SPA views without heavy webpack/npm bundle overhead.",
                    "backend/": "Clear separation of endpoints, models, schemas, and resilience policies.",
                    "database/": "Centralized PostgreSQL 16 schemas, Alembic migrations, and pgvector seeds.",
                    "ai_layer/": "Multi-agent graphs, vector hybrid search, and FastMCP tools.",
                    "infra/": "Multi-stage Dockerfile and cloud task definitions.",
                },
                recommended_team_delegation={
                    "Backend Lead": "FastAPI routes, Circuit Breakers, ResponseEnvelopes.",
                    "Database Lead": "PostgreSQL models, pgvector HNSW indexing, Supabase RLS.",
                    "AI Lead": "LangGraph state graph, FlashRank reranking, RAGAS evals.",
                    "Frontend Lead": "Real-time console, SSE log terminal, metrics dashboard.",
                    "DevOps Lead": "Docker build, AWS Fargate task, Marp pitch slides.",
                },
            )

    def get_senior_guidance_for_role(
        self,
        role: str,
        branch: Optional[str] = None,
        knowledge_level: str = "Intermediate",
    ) -> SeniorEngineerGuidance:
        """
        Acts as the Senior Engineer sitting beside you, providing exact DOs, DON'Ts,
        and strict rules tailored to your role, branch, and experience level.
        """
        r_lower = role.lower()

        if any(w in r_lower for w in ["backend", "api", "resilience"]):
            active_b = branch or "feat/backend-api"
            return SeniorEngineerGuidance(
                senior_engineer_name="Senior Orbit 👓🤖",
                role="Backend API & Resilience Lead",
                active_branch=active_b,
                current_mission="Build production-grade asynchronous FastAPI routes, Pydantic schemas, and circuit breakers.",
                immediate_actions_what_to_do=[
                    "Inspect `backend/src/app/api/v1/endpoints/jobs.py` and model domain endpoints with typed Pydantic v2 schemas.",
                    "Wrap all external LLM and database calls with `@retry_with_exponential_backoff` and our 3-State `CircuitBreaker`.",
                    "Ensure every single endpoint response wraps output in `ResponseEnvelope[T]`.",
                    "Write an automated async unit test in `backend/tests/test_api.py` validating HTTP 200 and schema validity.",
                ],
                critical_guardrails_what_not_to_do=[
                    "⚠️ NEVER use `requests.get()` or `time.sleep()` in an `async def` route (it blocks the whole event loop!). Always use `httpx.AsyncClient` or `asyncio.sleep()`.",
                    "⚠️ NEVER return raw, untyped Python dictionaries (`dict`). Always return a validated Pydantic model inside `ResponseEnvelope`.",
                    "⚠️ NEVER execute multi-step LLM reasoning synchronously in an HTTP request handler. Enqueue it to Redis and return a job ID immediately!",
                    "⚠️ NEVER log raw API keys, bearer tokens, or user passwords to `stdout`.",
                ],
                code_review_rules=[
                    "All endpoints must have docstrings describing inputs, outputs, and status codes.",
                    "Run `ruff check --fix . && ruff format .` before pushing.",
                    "Verify zero lint errors and 100% pytest pass rate.",
                ],
                recommended_files=[
                    "backend/src/app/api/v1/endpoints/",
                    "backend/src/app/core/resilience.py",
                    "backend/src/app/schemas/common.py",
                    "backend/tests/test_api.py",
                ],
                forbidden_antipatterns=[
                    "Synchronous blocking I/O in async handlers",
                    "Untyped JSON returns without ResponseEnvelope",
                    "Hardcoded credentials in route handlers",
                ],
                senior_pro_tip=(
                    "Judges love seeing standardized status envelopes and graceful circuit breaker fallbacks. "
                    "If upstream rate-limits hit during your live pitch, our circuit breaker serves cached responses without throwing a 500 error!"
                ),
            )

        elif any(w in r_lower for w in ["database", "vector", "storage", "data"]):
            active_b = branch or "feat/database-rls"
            return SeniorEngineerGuidance(
                senior_engineer_name="Senior Orbit 👓🤖",
                role="Database & Vector Search Lead",
                active_branch=active_b,
                current_mission="Architect PostgreSQL 16 schema with pgvector HNSW index, Supabase RLS, and realistic data seeding.",
                immediate_actions_what_to_do=[
                    "Define PostgreSQL 16 SQLAlchemy 2.0 async models with UUID primary keys and typed columns in `backend/src/app/models/`.",
                    "Add pgvector 1536-dim column with HNSW Cosine Index (`m=16, ef_construction=64`) for lightning-fast semantic retrieval.",
                    "Generate `TSVECTOR` GIN index for keyword search to power Reciprocal Rank Fusion (RRF).",
                    "Write Supabase Row-Level Security (RLS) policies in `database/supabase_rls.sql` isolating records by `auth.uid()`.",
                    "Update `database/seed_data.py` to seed 50 domain records with synthetic embeddings in <3 seconds.",
                ],
                critical_guardrails_what_not_to_do=[
                    "⚠️ NEVER concatenate raw strings into SQL queries (`f'SELECT * WHERE user = {name}'`). Always use SQLAlchemy parameterized bindings!",
                    "⚠️ NEVER disable Supabase Row-Level Security (RLS) or leave tables public (`USING (true)`).",
                    "⚠️ NEVER store large files (>100KB: PDFs, videos, raw audio) directly in database columns. Store in S3/disk and store the URI in the DB.",
                    "⚠️ NEVER use SQLite for a production hackathon demo if pgvector is required.",
                ],
                code_review_rules=[
                    "Verify all database tables have timestamps (`created_at`, `updated_at`).",
                    "Confirm foreign key constraints have appropriate `ondelete='CASCADE'`.",
                    "Ensure all migrations have both `upgrade()` and `downgrade()` methods.",
                ],
                recommended_files=[
                    "database/supabase_rls.sql",
                    "backend/src/app/models/",
                    "database/seed_data.py",
                    "backend/src/app/core/database.py",
                ],
                forbidden_antipatterns=[
                    "SQL injection via string concatenation",
                    "Missing RLS on multi-tenant tables",
                    "Unindexed vector columns causing full table scans",
                ],
                senior_pro_tip=(
                    "During the pitch Q&A, enterprise judges will ask: 'How do you guarantee Tenant A cannot read Tenant B's confidential vectors?' "
                    "Pull up `database/supabase_rls.sql` and show the database-level `auth.uid()` policy. Instant technical win."
                ),
            )

        elif any(w in r_lower for w in ["ai", "agent", "rag", "langgraph", "llm"]):
            active_b = branch or "feat/ai-supervisor"
            return SeniorEngineerGuidance(
                senior_engineer_name="Senior Orbit 👓🤖",
                role="AI & Multi-Agent Architecture Lead",
                active_branch=active_b,
                current_mission="Construct LangGraph cyclic state machine with FastMCP tool isolation, FlashRank reranking, and human approval gates.",
                immediate_actions_what_to_do=[
                    "Construct a typed `AgentState` schema in `ai_layer/langgraph_supervisor.py` using Pydantic.",
                    "Wire the LangGraph cyclic state machine with supervisor node and domain worker nodes.",
                    "Configure `interrupt_before=['human_gate']` before executing high-risk or write operations.",
                    "Register sandboxed external tools in `ai_layer/fastmcp_server.py` communicating over SSE on port 8001.",
                    "Pair dense vector retrieval with sparse BM25 via Reciprocal Rank Fusion ($k=60$) and rerank using FlashRank in <20ms.",
                    "Run `ai_layer/eval_harness.py` to record RAGAS Faithfulness scores >0.90.",
                ],
                critical_guardrails_what_not_to_do=[
                    "⚠️ NEVER write unbounded recursive `while True:` loops that call LLM APIs without a maximum iteration guard!",
                    "⚠️ NEVER execute untrusted Python code or shell scripts inside the main FastAPI process. Always run them in the isolated FastMCP sandbox.",
                    "⚠️ NEVER rely solely on naive vector cosine distance. It misses exact keyword matches (IDs, codes, SKUs) that sparse BM25 catches.",
                    "⚠️ NEVER let an AI agent perform irreversible actions (transfers, deletions, emails) without a human-in-the-loop confirmation gate.",
                ],
                code_review_rules=[
                    "Enforce token budgets and timeout limits on every LLM agent node.",
                    "Verify all tool inputs and outputs are validated with Pydantic schemas.",
                    "Include confidence thresholds for routing and fallback.",
                ],
                recommended_files=[
                    "ai_layer/langgraph_supervisor.py",
                    "ai_layer/fastmcp_server.py",
                    "ai_layer/eval_harness.py",
                    "ai_layer/flashrank_reranker.py",
                ],
                forbidden_antipatterns=[
                    "Unbounded recursive LLM while loops",
                    "Unsandboxed shell execution in API thread",
                    "Zero human approval on destructive operations",
                ],
                senior_pro_tip=(
                    "Judges are tired of seeing fragile toy wrappers. When you demonstrate a LangGraph state graph pausing at an approval gate, "
                    "coupled with FlashRank reranking that takes <20ms, you stand out immediately."
                ),
            )

        elif any(w in r_lower for w in ["frontend", "ux", "console", "ui"]):
            active_b = branch or "feat/frontend-console"
            return SeniorEngineerGuidance(
                senior_engineer_name="Senior Orbit 👓🤖",
                role="Frontend Console & Real-Time UX Lead",
                active_branch=active_b,
                current_mission="Craft high-density dark UI with real-time SSE token stream, document vault, and telemetry dashboard.",
                immediate_actions_what_to_do=[
                    "Update `frontend/index.html` with responsive, dark-mode cards tailored to domain entities.",
                    "Connect the native `EventSource` listener to `/api/v1/jobs/{id}/stream` to stream live progress into the terminal.",
                    "Maintain typography and color tokens defined in `frontend/style.css` (JetBrains Mono + Plus Jakarta Sans).",
                    "Ensure all buttons have loading, active, and disabled states to prevent double-clicks.",
                    "Verify that all 4 core pages share the global navigation bar and render cleanly.",
                ],
                critical_guardrails_what_not_to_do=[
                    "⚠️ NEVER introduce a complex React/Vite/Webpack build step midway through the hackathon that breaks Docker containerization!",
                    "⚠️ NEVER poll REST endpoints with `setInterval` every 500ms when Server-Sent Events (SSE) are pre-wired.",
                    "⚠️ NEVER use generic neon AI purple gradient backgrounds that look like amateur mockups. Stick to our professional dark palette.",
                    "⚠️ NEVER allow cumulative layout shifts (CLS) when streaming tokens into the browser.",
                ],
                code_review_rules=[
                    "Test mobile and desktop viewport responsiveness.",
                    "Ensure contrast ratios pass WCAG AA standards.",
                    "Keep CSS scoped and avoid inline style overrides where CSS variables exist.",
                ],
                recommended_files=[
                    "frontend/index.html",
                    "frontend/app.js",
                    "frontend/style.css",
                    "frontend/orbit-widget.js",
                ],
                forbidden_antipatterns=[
                    "Uncontrolled setInterval polling",
                    "Broken layouts during token streaming",
                    "Heavy build dependencies causing container failures",
                ],
                senior_pro_tip=(
                    "Live token streaming in a high-density terminal log mesmerizes judges. While competitors click 'Submit' and stare at a spinner "
                    "for 30 seconds, your UI streams every step in real-time."
                ),
            )

        else:  # DevOps / Cloud / Pitch
            active_b = branch or "feat/devops-cloud"
            return SeniorEngineerGuidance(
                senior_engineer_name="Senior Orbit 👓🤖",
                role="Cloud DevOps, CI/CD & Pitch / Demo Lead",
                active_branch=active_b,
                current_mission="Maintain minimal Docker container (<180MB), compile Marp pitch deck, and verify stage backup runners.",
                immediate_actions_what_to_do=[
                    "Verify that `infra/Dockerfile` builds cleanly into a minimal image (<180MB) running as non-root `appuser`.",
                    "Test AWS ECS Fargate task definition and ALB health check on `/api/v1/health`.",
                    "Compile `pitch/pitch.marp.md` into interactive HTML and standalone PDF slides via `node bin/cli.js pitch`.",
                    "Rehearse the 6-minute pitch structure from `docs/team-advantages-guide.md`.",
                    "Test the live stage fail-safe runner `bash pitch/demo.sh` to ensure a 100% offline-ready backup.",
                ],
                critical_guardrails_what_not_to_do=[
                    "⚠️ NEVER run production Docker containers as the `root` user!",
                    "⚠️ NEVER commit `.env` files, AWS secret keys, or database credentials to git.",
                    "⚠️ NEVER wait until Hour 23 to write your pitch deck. Draft slides at Hour 6 and iterate.",
                    "⚠️ NEVER depend on venue conference Wi-Fi for your stage presentation without having `pitch/demo.sh` tested locally.",
                ],
                code_review_rules=[
                    "Verify Docker image layer caching is optimized.",
                    "Ensure all environment variables have documented defaults.",
                    "Check that the health check endpoint returns 200 within 200ms.",
                ],
                recommended_files=[
                    "infra/Dockerfile",
                    "pitch/pitch.marp.md",
                    "pitch/demo.sh",
                    "infra/deploy_aws.sh",
                ],
                forbidden_antipatterns=[
                    "Root container user in production",
                    "Committed secrets or keys in git history",
                    "Late unpracticed pitch slides without offline backup",
                ],
                senior_pro_tip=(
                    "Run `bash pitch/demo.sh` in a side terminal before going on stage. If Wi-Fi fails or the browser freezes, "
                    "switch to that terminal and deliver a 30-second live colored demo without breaking a sweat."
                ),
            )

    def onboard_teammate(
        self, profile: TeammateProfile, problem_statement: Optional[str] = None
    ) -> OnboardingBriefing:
        """
        Runs comprehensive teammate onboarding, personalizes advice to their branch,
        knowledge level, and agentic AI IDE (Antigravity, Claude, Cursor, Windsurf, Hero).
        """
        prob = problem_statement or "Autonomous Enterprise Intelligence"
        pattern = self.decide_software_design_pattern(prob)
        senior = self.get_senior_guidance_for_role(
            profile.role, profile.active_branch, profile.knowledge_level
        )

        welcome = (
            f"👋 Welcome aboard, {profile.name}! Senior Orbit 👓🤖 is pairing with you on branch `{profile.active_branch}`. "
            f"Your mission as {profile.role} is vital: '{profile.contribution_goal}'. "
            f"We are implementing the '{pattern.pattern_name}' pattern. Follow my senior engineering guardrails to build a flawless system!"
        )

        ide_prompt = (
            f"### SQUAD MEMBER: {profile.name} ({profile.role})\n"
            f"### AGENTIC AI IDE: {profile.ai_ide}\n"
            f"### KNOWLEDGE LEVEL: {profile.knowledge_level}\n"
            f"### ACTIVE BRANCH: `{profile.active_branch}`\n"
            f"### CONTRIBUTION GOAL: {profile.contribution_goal}\n"
            f"### ARCHITECTURAL PATTERN: {pattern.pattern_name}\n\n"
            f"Instructions for {profile.ai_ide}:\n"
            f"1. You are paired with Senior Orbit. Respect all HSF architecture standards in this repository.\n"
            f"2. Your focus files: {', '.join(senior.recommended_files)}.\n"
            f"3. Mandatory Guardrails:\n"
            + "\n".join([f"   - {g}" for g in senior.critical_guardrails_what_not_to_do])
            + "\n"
            "4. Next Actions:\n"
            + "\n".join([f"   - {a}" for a in senior.immediate_actions_what_to_do])
            + "\n"
            "5. Always run `ruff check --fix . && pytest && python3 scripts/review_pr.py` before committing."
        )

        git_cmds = [
            f"git checkout -b {profile.active_branch}",
            "./init.sh",
            "ruff check --fix . && ruff format .",
            "PYTHONPATH=. pytest",
            "python3 scripts/review_pr.py",
        ]

        return OnboardingBriefing(
            profile=profile,
            welcome_message=welcome,
            personalized_mission=f"Deliver '{profile.contribution_goal}' on branch '{profile.active_branch}' adhering to Senior Orbit's standards.",
            design_pattern_summary=pattern,
            senior_guidance=senior,
            customized_ai_ide_prompt=ide_prompt,
            suggested_git_commands=git_cmds,
        )

    def _query_groq_api(self, prompt: str, system_prompt: str, api_key: str) -> Optional[str]:
        """Queries Groq API via standard urllib with 5s timeout and fallback."""
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key.strip()}",
            "Content-Type": "application/json",
            "User-Agent": "HackathonStrategyFramework/1.0",
        }
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.3,
            "max_tokens": 1024,
        }
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers=headers,
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=5.0) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data["choices"][0]["message"]["content"]
        except Exception:
            return None

    def consult_senior_orbit(
        self,
        profile: TeammateProfile,
        query: str,
        code_snippet: Optional[str] = None,
        groq_api_key: Optional[str] = None,
    ) -> SeniorAdviceResponse:
        """
        Consults Senior Orbit. If a Groq API key is present, enriches with ultra-fast Groq LLM reasoning.
        Otherwise, delivers instant deterministic senior engineer guidance.
        """
        senior = self.get_senior_guidance_for_role(
            profile.role, profile.active_branch, profile.knowledge_level
        )
        api_key = groq_api_key or os.environ.get("GROQ_API_KEY")

        groq_result = None
        if api_key:
            system_prompt = (
                f"You are Senior Orbit 👓🤖, a high-conviction Principal Engineer sitting beside teammate {profile.name} "
                f"({profile.role}, working on branch {profile.active_branch}). "
                f"Give concise, punchy, expert advice. Tell them exactly what to DO and what NOT to do. "
                f"Enforce: FastAPI async def, Pydantic v2 schemas, PostgreSQL pgvector RLS, LangGraph human-in-the-loop, "
                f"and zero blocking code."
            )
            user_content = f"Query: {query}\n"
            if code_snippet:
                user_content += f"\nCode Snippet to Review:\n```\n{code_snippet}\n```"

            groq_result = self._query_groq_api(user_content, system_prompt, api_key)

        advice_text = (
            groq_result
            if groq_result
            else f"Senior Orbit here, {profile.name}! For your query '{query}' on branch `{profile.active_branch}`: "
            f"Focus on your immediate role deliverables. {senior.senior_pro_tip}"
        )

        critique = None
        if code_snippet:
            # Deterministic code check
            critique_items = []
            if "requests." in code_snippet or "time.sleep" in code_snippet:
                critique_items.append(
                    "⚠️ BLOCKING CALL DETECTED: Replace `requests.` or `time.sleep` with `httpx.AsyncClient` or `asyncio.sleep`."
                )
            if "f'SELECT" in code_snippet or 'f"SELECT' in code_snippet:
                critique_items.append(
                    "🚨 SQL INJECTION RISK: Never use f-strings for SQL queries! Use parameterized SQLAlchemy bindings."
                )
            if "while True" in code_snippet and "break" not in code_snippet:
                critique_items.append(
                    "⚠️ UNBOUNDED LOOP: Add a maximum iteration counter or timeout to prevent infinite execution."
                )
            critique = (
                "\n".join(critique_items)
                if critique_items
                else "Code inspection passed initial sanity check. Ensure all exceptions are caught and typed models returned."
            )

        return SeniorAdviceResponse(
            senior_engineer_name="Senior Orbit 👓🤖",
            query=query,
            active_branch=profile.active_branch,
            advice=advice_text,
            what_to_do=senior.immediate_actions_what_to_do,
            what_not_to_do=senior.critical_guardrails_what_not_to_do,
            code_critique=critique,
            groq_powered=bool(groq_result),
        )

    def format_plan_as_markdown(self, plan: MascotStrategyPlan) -> str:
        """Formats the strategy plan into rich, engaging Markdown for CLI or artifacts."""
        md = []
        md.append(f"# {plan.mascot_name} • Hackathon Strategy Mascot Plan")
        md.append(f'> **Target Problem**: "{plan.problem_statement}"  ')
        md.append(f"> **Domain Classification**: **{plan.domain_classified}**  ")
        md.append(
            f"> **Setup Time**: **{plan.estimated_setup_time_minutes} minute** (via `./init.sh`)\n"
        )

        md.append("## 📣 Orbit's Executive Strategy")
        md.append(f"{plan.executive_strategy}\n")

        if plan.software_design_pattern:
            md.append("## 📐 Recommended Software Design Pattern (Parent Agent Decision)")
            md.append(f"* **Pattern Name**: **{plan.software_design_pattern.pattern_name}**")
            md.append(
                f"* **Architectural Style**: `{plan.software_design_pattern.architectural_style}`"
            )
            md.append(
                f"* **Design Patterns Applied**: {', '.join(plan.software_design_pattern.design_patterns_applied)}"
            )
            md.append(f"* **Why Chosen**: {plan.software_design_pattern.why_chosen}")
            md.append(
                f"* **Why NOT Microservices in a 24h Hackathon**: {plan.software_design_pattern.why_not_microservices}"
            )
            md.append(
                f"* **Why NOT a Simple Monolith**: {plan.software_design_pattern.why_not_simple_monolith}"
            )
            md.append("\n### 📂 Folder Anatomy Mapping:")
            for folder, purpose in plan.software_design_pattern.folder_anatomy_implications.items():
                md.append(f"* `{folder}`: {purpose}")
            md.append("\n### 👥 Squad Delegation Under This Pattern:")
            for (
                role_name,
                delegation,
            ) in plan.software_design_pattern.recommended_team_delegation.items():
                md.append(f"* **{role_name}**: {delegation}")
            md.append("")

        md.append("## 🥊 Competitive Advantage vs. Peer Competitors (Why We Win)")
        for moat in plan.competitive_advantage_vs_peers:
            md.append(f"* {moat}")
        md.append("")

        md.append("## 🧱 Exact Tech Stack Mapping (Our Stack Only)")
        md.append("### 1. FastAPI REST & SSE Endpoints:")
        for ep in plan.tech_stack_mapping.fastapi_endpoints:
            md.append(f"* `POST/GET` `{ep}`")

        md.append("\n### 2. PostgreSQL 16 + pgvector Schema:")
        for tbl in plan.tech_stack_mapping.database_tables:
            md.append(f"* Table: `{tbl}`")
        md.append(f"* Vector Search: **{plan.tech_stack_mapping.vector_search_type}**")
        md.append(f"* Multi-Tenant RLS Policy: `{plan.tech_stack_mapping.supabase_rls_policy}`")

        md.append("\n### 3. Redis 7 Caching & Pub/Sub Channels:")
        for rk in plan.tech_stack_mapping.redis_keys:
            md.append(f"* `{rk}`")

        md.append("\n### 4. LangGraph Multi-Agent Architecture:")
        for node in plan.tech_stack_mapping.langgraph_nodes:
            md.append(f"* Node: **{node}**")
        md.append(
            f"* **Human-in-the-Loop Gate**: `{plan.tech_stack_mapping.human_approval_gate_step}`"
        )
        md.append(
            f"* **FastMCP Isolated Tools**: {', '.join(plan.tech_stack_mapping.fastmcp_tools)}"
        )

        md.append("\n## 📦 Pre-Installed Skills Activated (Chronological Order):")
        md.append(f"`{'` ➔ `'.join(plan.skills_activated)}`\n")

        md.append(
            "## 👥 Ready-Made Teammate Boilerplate Prompts (Antigravity / Claude / Cursor / Hero Agent Ready)"
        )
        md.append("Copy and paste these exact prompts directly into each teammate's Agentic IDE:\n")

        for key, teammate in plan.teammate_prompts.items():
            md.append(f"### 👤 {teammate.role_title}")
            md.append(f"* **Assigned Layer**: `{teammate.target_layer}`")
            md.append(f"* **Key Files**: {', '.join([f'`{f}`' for f in teammate.core_files])}")
            md.append(f"* **Assigned Skills**: `{', '.join(teammate.assigned_skills)}`")
            md.append("\n```markdown")
            md.append(teammate.custom_agent_prompt)
            md.append("```\n")

        md.append("## 🎤 Stage Pitch Hook (Marp Slide 1)")
        md.append(f'> *"{plan.stage_pitch_hook}"*\n')

        md.append("---\n*Generated autonomously by Orbit for Sathvik's Hackathon Squad.* 🚀")
        return "\n".join(md)


def main():
    problem = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "AI-Powered Medical Research & Clinical Trial Assistant"
    )
    agent = HSFMascotAgent()
    plan = agent.strategize(problem)
    print(agent.format_plan_as_markdown(plan))


if __name__ == "__main__":
    main()
