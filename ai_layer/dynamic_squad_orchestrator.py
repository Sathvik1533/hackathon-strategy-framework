"""
HSF Transformers Dynamic Squad Orchestrator & Universal Features Menu Engine
(ai_layer/dynamic_squad_orchestrator.py)

Autonomous orchestrator modeling the Transformers Robot Squad:
- Orbit Prime (Supreme Commander & Master Architect)
- Ironhide (Backend Titan & Resilience Sentinel)
- Mirage (Frontend UI Hologram Specialist)
- Wheeljack (AI & Multi-Agent Weaponsmith)
- Ratchet (Database & Security Guardian)
- Bumblebee (Cloud DevOps & Stage Scout)

Dynamically adapts to variable team sizes (1 to 6+ teammates), assigns robot companions,
generates a comprehensive "Features Menu" across all 5 technical layers for any problem statement,
and integrates with DynamicSkillRegistry and OrbitMemoryTracer.
"""

from __future__ import annotations

import os
import re
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from ai_layer.mascot_agent import (
    FrontendAestheticDecision,
    HSFMascotAgent,
    SoftwareDesignPatternDecision,
    TeammateProfile,
)
from ai_layer.orbit_memory_tracer import OrbitMemoryTracer
from ai_layer.skill_registry import DynamicSkillRegistry


class RobotAutobot(BaseModel):
    codename: str  # e.g., "Orbit Prime", "Ironhide", "Mirage", "Wheeljack", "Ratchet", "Bumblebee"
    callsign: str  # e.g., "The Supreme Architect", "The Resilience Titan"
    avatar_emoji: str
    primary_domain: str
    target_layer: str
    core_responsibilities: List[str]
    assigned_skills: List[str]
    motto: str
    anti_patterns_guarded: List[str]


class TeamMemberAssignment(BaseModel):
    teammate_name: str
    assigned_role: str
    assigned_layers: List[str]
    companion_robot: RobotAutobot
    teammate_knowledge_level: str = "Intermediate"
    custom_ide_prompt: str
    git_branch: str
    starter_checklist: List[str]


class LayerFeaturesMenu(BaseModel):
    layer_name: str  # Frontend, Backend, Database, AI & Multi-Agent, Cloud & DevOps
    executive_summary: str
    core_features: List[Dict[str, Any]]
    recommended_libraries: List[str]
    performance_budget: str
    security_and_compliance: str


class FullSystemFeaturesMenu(BaseModel):
    problem_statement: str
    domain: str
    frontend_menu: LayerFeaturesMenu
    backend_menu: LayerFeaturesMenu
    database_menu: LayerFeaturesMenu
    ai_agentic_menu: LayerFeaturesMenu
    devops_cloud_menu: LayerFeaturesMenu


class SquadOrchestrationResult(BaseModel):
    problem_statement: str
    detected_domain: str
    team_size: int
    team_strategy_archetype: str
    design_pattern: SoftwareDesignPatternDecision
    frontend_aesthetic: FrontendAestheticDecision
    robot_squad: List[RobotAutobot]
    teammate_assignments: List[TeamMemberAssignment]
    features_menu: FullSystemFeaturesMenu
    memory_trace_id: Optional[str] = None


# Define the 6 Canonical Transformers Autobots
TRANSFORMERS_ROBOTS: Dict[str, RobotAutobot] = {
    "orbit_prime": RobotAutobot(
        codename="Orbit Prime 🤖👑",
        callsign="Supreme Commander & Master Architect",
        avatar_emoji="🤖",
        primary_domain="System Architecture & Strategy",
        target_layer="Orchestration & Governance",
        core_responsibilities=[
            "Decomposes problem statements into modular specifications",
            "Enforces software design patterns (Hexagonal / Event-Driven / CQRS)",
            "Coordinates multi-agent workflows and resolves inter-layer contract disputes",
            "Monitors hackathon countdown clock and MVP delivery gates",
        ],
        assigned_skills=[
            "hackathon-speedrun-kit",
            "jev-decision-router",
            "hallmark",
        ],
        motto="Autobots, roll out! Zero wasted minutes, zero technical debt.",
        anti_patterns_guarded=[
            "Unfocused scope creep during the final 4 hours",
            "Mismatch between backend API contracts and frontend views",
        ],
    ),
    "ironhide": RobotAutobot(
        codename="Ironhide 🛡️⚡",
        callsign="Backend Titan & Resilience Sentinel",
        avatar_emoji="🛡️",
        primary_domain="High-Throughput APIs & Distributed Reliability",
        target_layer="Backend API & Middleware",
        core_responsibilities=[
            "Implements async FastAPI route handlers with ResponseEnvelope[T]",
            "Maintains Redis connection pooling, distributed SETNX mutex locks, and rate limits",
            "Configures circuit breakers (3 fails -> OPEN, 30s cooldown)",
            "Streams server-sent events (SSE) for real-time progress updates",
        ],
        assigned_skills=[
            "fastapi-production-archetype",
            "async-agent-celery-redis",
            "llm-gateway-semantic-cache",
        ],
        motto="My circuits do not break. Throughput stays high, latency stays low.",
        anti_patterns_guarded=[
            "Synchronous time.sleep() or blocking requests.get() inside async routes",
            "Unbounded memory leaks and unhandled 500 internal server errors",
        ],
    ),
    "mirage": RobotAutobot(
        codename="Mirage 🎨✨",
        callsign="Frontend Hologram Specialist",
        avatar_emoji="🎨",
        primary_domain="Visual Design & Micro-Interactions",
        target_layer="Frontend & User Experience",
        core_responsibilities=[
            "Executes 1 of 5 aesthetic paradigms (Skeuomorphism, Claymorphism, Glassmorphism, Neo-Brutalism, Industrial Brutalism)",
            "Guarantees zero layout shift with Next.js 14 App Router and Tailwind CSS",
            "Applies Emil Kowalski motion tokens (spring physics, ease-out-expo)",
            "Builds responsive, accessibility-first interfaces that mesmerize judges in 3 seconds",
        ],
        assigned_skills=[
            "hallmark",
            "context7-docs-fetcher",
        ],
        motto="If the interface does not inspire in 3 seconds, the battle is already lost.",
        anti_patterns_guarded=[
            "Generic purple-gradient AI-slop with harsh box shadows",
            "Flickering layouts and unresponsive mobile viewports",
        ],
    ),
    "wheeljack": RobotAutobot(
        codename="Wheeljack 🔬⚡",
        callsign="AI & Multi-Agent Weaponsmith",
        avatar_emoji="🔬",
        primary_domain="Cognitive State Machines & Neural Search",
        target_layer="AI Layer & Multi-Agent",
        core_responsibilities=[
            "Builds LangGraph cyclic state machines with human-in-the-loop review gates",
            "Deploys FastMCP tool servers exposing JSON-RPC over Server-Sent Events",
            "Optimizes FlashRank neural rerankers (top 5 in <20ms)",
            "Executes RAGAS evaluation harnesses tracking faithfulness and answer relevancy",
        ],
        assigned_skills=[
            "langgraph-production-patterns",
            "fastmcp-tool-server",
            "pydantic-ai-workflows",
            "rag-reranking-pipeline",
            "agent-security-guardrails",
            "agent-eval-harness",
        ],
        motto="Pure engineering brilliance! State graphs with deterministic execution.",
        anti_patterns_guarded=[
            "Unconstrained recursive agent loops that exhaust token budgets",
            "Hallucinated citations without ground-truth vector retrieval",
        ],
    ),
    "ratchet": RobotAutobot(
        codename="Ratchet 🏥💾",
        callsign="Database & Security Guardian",
        avatar_emoji="💾",
        primary_domain="Vector Indexing, ACID Integrity & Row-Level Security",
        target_layer="Database & Storage",
        core_responsibilities=[
            "Designs PostgreSQL 16 schemas with strict foreign keys and audit trails",
            "Builds pgvector HNSW cosine indexes fused with BM25 via Reciprocal Rank Fusion",
            "Configures Supabase Row-Level Security (RLS) policies protecting tenant data",
            "Monitors connection pool saturation and query execution plans",
        ],
        assigned_skills=[
            "pgvector-hybrid-search",
            "agent-security-guardrails",
        ],
        motto="Data integrity is non-negotiable. Not a single byte compromised.",
        anti_patterns_guarded=[
            "Sequential table scans on vector embeddings without HNSW indexes",
            "Hardcoded API secrets or missing RLS tenant filters",
        ],
    ),
    "bumblebee": RobotAutobot(
        codename="Bumblebee 🐝🚀",
        callsign="Cloud DevOps & Stage Scout",
        avatar_emoji="🚀",
        primary_domain="Containerization, Cloud CI/CD & Live Presentation",
        target_layer="Cloud DevOps & Presentation",
        core_responsibilities=[
            "Builds multi-stage Docker containers under 180MB with non-root security",
            "Authors AWS ECS Fargate task definitions and zero-downtime blue/green rollouts",
            "Generates offline-first demo scripts (demo.sh) that never fail on stage Wi-Fi",
            "Crafts Marp presentation decks highlighting market moats and ROI",
        ],
        assigned_skills=[
            "agent-docker-aws-deploy",
            "poetry-python-packaging",
            "marp-presentation-engine",
        ],
        motto="Fast, nimble, reliable. The live demo will never crash on stage.",
        anti_patterns_guarded=[
            "Bloated 1.5GB Docker images that take 10 minutes to pull on stage",
            "Live demo crashing due to reliance on un-mocked external Wi-Fi APIs",
        ],
    ),
}


class DynamicSquadOrchestrator:
    """
    Main Orchestrator engine coordinating the Transformers Robot Squad,
    adapting to variable team sizes (1 to 6+), generating the Universal Features Menu,
    and recording developer telemetry traces into Orbit's learning memory.
    """

    def __init__(self, data_dir: str = ".hsf"):
        self.mascot_agent = HSFMascotAgent()
        self.skill_registry = DynamicSkillRegistry(storage_dir=os.path.join(data_dir, "skills"))
        self.memory_tracer = OrbitMemoryTracer(data_dir=data_dir)

    def orchestrate_squad(
        self,
        problem_statement: str,
        team_size: int = 5,
        teammate_profiles: Optional[List[TeammateProfile]] = None,
    ) -> SquadOrchestrationResult:
        """
        Orchestrates the Autobot squad and assigns roles tailored to the exact team size.
        """
        # Clamp team size
        actual_size = max(1, min(10, team_size))
        domain = self.mascot_agent._infer_domain(problem_statement)
        design_pattern = self.mascot_agent.decide_software_design_pattern(problem_statement)
        aesthetic = self.mascot_agent.decide_frontend_aesthetic(problem_statement)

        # 1. Determine team strategy archetype
        archetype_map = {
            1: "Solo Pioneer (Fullstack + Autonomous Robot Co-Pilots)",
            2: "Dynamic Duo (Product & UX Lead + AI & Data Architect)",
            3: "Trio Strike Team (Frontend Lead + Backend Lead + AI & Data Lead)",
            4: "Core Four (Frontend Lead + Backend Lead + AI Lead + Data & DevOps Lead)",
            5: "Full Pentad (Frontend + Backend + AI + Database + Cloud/DevOps)",
        }
        archetype = archetype_map.get(
            actual_size,
            f"Extended League of {actual_size} (Specialized Feature Pods + QA/Pitch Leads)",
        )

        # 2. Build Teammate Assignments based on size
        assignments = self._build_variable_assignments(
            actual_size,
            teammate_profiles,
            problem_statement,
            design_pattern,
            aesthetic,
        )

        # 3. Generate Full Layer Features Menu
        features_menu = self.generate_features_menu(problem_statement, domain, aesthetic)

        # 4. Record trace in Orbit Memory
        lead_name = teammate_profiles[0].name if teammate_profiles else "Lead Developer"
        trace = self.memory_tracer.log_trace(
            teammate_name=lead_name,
            role="Squad Lead",
            active_branch="main",
            action_type="ARCHITECTURE_DECISION",
            query_or_task=f"Orchestrated {actual_size}-person Transformers Squad for: {problem_statement[:60]}...",
            guidance_rendered=(
                f"Activated {archetype}. Assigned {len(assignments)} teammates with Autobot companions. "
                f"Selected {aesthetic.aesthetic_name} aesthetic and {design_pattern.pattern_name} pattern."
            ),
            detected_risks=[
                "Ensure team adheres to assigned git branches to prevent merge conflicts",
                "Execute local Docker test before hackathon submission",
            ],
            outcome_status="RESOLVED",
        )

        return SquadOrchestrationResult(
            problem_statement=problem_statement,
            detected_domain=domain,
            team_size=actual_size,
            team_strategy_archetype=archetype,
            design_pattern=design_pattern,
            frontend_aesthetic=aesthetic,
            robot_squad=list(TRANSFORMERS_ROBOTS.values()),
            teammate_assignments=assignments,
            features_menu=features_menu,
            memory_trace_id=trace.trace_id,
        )

    def _build_variable_assignments(
        self,
        team_size: int,
        provided_profiles: Optional[List[TeammateProfile]],
        problem_statement: str,
        design_pattern: SoftwareDesignPatternDecision,
        aesthetic: FrontendAestheticDecision,
    ) -> List[TeamMemberAssignment]:
        """
        Calculates role divisions and pairs each teammate with an Autobot companion.
        """
        assignments: List[TeamMemberAssignment] = []

        # Standard default roles per team size configuration
        if team_size == 1:
            name = provided_profiles[0].name if provided_profiles else "Solo Builder"
            level = provided_profiles[0].knowledge_level if provided_profiles else "Senior"
            assignments.append(
                TeamMemberAssignment(
                    teammate_name=name,
                    assigned_role="Fullstack Pioneer & Supreme Commander",
                    assigned_layers=["Frontend", "Backend", "AI Layer", "Database", "Cloud DevOps"],
                    companion_robot=TRANSFORMERS_ROBOTS["orbit_prime"],
                    teammate_knowledge_level=level,
                    git_branch="feat/solo-mvp",
                    custom_ide_prompt=(
                        f"You are the Solo Builder paired with Orbit Prime and the entire Autobot Squad. "
                        f"Problem: {problem_statement}. Architectural Pattern: {design_pattern.pattern_name}. "
                        f"Aesthetic: {aesthetic.aesthetic_name}. "
                        f"Use our pre-ready FastAPI backend, LangGraph AI workflow, pgvector database, and Next.js frontend. "
                        f"Execute modular vertical slices from database schema to UI in single commits."
                    ),
                    starter_checklist=[
                        "Verify Docker environment: docker compose up -d postgres redis",
                        "Start FastAPI backend: poetry run uvicorn backend.src.app.main:app --reload",
                        "Verify Next.js dashboard: cd mascot-dashboard && npm run dev",
                        "Test hybrid vector query: curl http://localhost:8000/api/v1/health",
                    ],
                )
            )

        elif team_size == 2:
            p1_name = (
                provided_profiles[0].name
                if provided_profiles and len(provided_profiles) > 0
                else "Alex"
            )
            p2_name = (
                provided_profiles[1].name
                if provided_profiles and len(provided_profiles) > 1
                else "Sam"
            )
            assignments.append(
                TeamMemberAssignment(
                    teammate_name=p1_name,
                    assigned_role="Product & Fullstack UX Lead",
                    assigned_layers=["Frontend UI", "Backend Core API", "Presentation"],
                    companion_robot=TRANSFORMERS_ROBOTS["mirage"],
                    teammate_knowledge_level="Intermediate",
                    git_branch="feat/product-ux-core",
                    custom_ide_prompt=(
                        f"You are {p1_name}, paired with Mirage and Ironhide. "
                        f"Build the user-facing interface using {aesthetic.aesthetic_name} and connect to FastAPI routes. "
                        f"Deliver high visual polish and sub-100ms UI interactions."
                    ),
                    starter_checklist=[
                        "Implement UI screens adhering to aesthetic design tokens",
                        "Wire SSE event listener to /api/v1/jobs/{id}/stream",
                        "Prepare Marp presentation deck slides (pitch/pitch.marp.md)",
                    ],
                )
            )
            assignments.append(
                TeamMemberAssignment(
                    teammate_name=p2_name,
                    assigned_role="AI Systems, Database & Cloud Architect",
                    assigned_layers=["AI Multi-Agent", "pgvector Database", "DevOps/Infra"],
                    companion_robot=TRANSFORMERS_ROBOTS["wheeljack"],
                    teammate_knowledge_level="Senior",
                    git_branch="feat/ai-data-engine",
                    custom_ide_prompt=(
                        f"You are {p2_name}, paired with Wheeljack and Ratchet. "
                        f"Build the LangGraph state machine, FastMCP server, and pgvector HNSW hybrid search. "
                        f"Deploy containerized infrastructure via Docker."
                    ),
                    starter_checklist=[
                        "Define PostgreSQL table schema and pgvector HNSW indexes",
                        "Implement LangGraph supervisor graph with human approval gate",
                        "Verify test coverage with pytest and check Docker build size",
                    ],
                )
            )

        elif team_size == 3:
            names = [
                provided_profiles[i].name
                if provided_profiles and len(provided_profiles) > i
                else f"Teammate {i + 1}"
                for i in range(3)
            ]
            assignments.append(
                TeamMemberAssignment(
                    teammate_name=names[0],
                    assigned_role="Frontend & Interaction Lead",
                    assigned_layers=["Frontend UI", "Aesthetic Design Tokens", "Client State"],
                    companion_robot=TRANSFORMERS_ROBOTS["mirage"],
                    git_branch="feat/frontend-views",
                    custom_ide_prompt=(
                        f"Lead Frontend with Mirage. Implement {aesthetic.aesthetic_name} style. "
                        f"Zero layout shift, responsive tables, real-time SSE chart widgets."
                    ),
                    starter_checklist=[
                        "Configure design tokens and CSS variables",
                        "Implement primary workflow dashboard screens",
                        "Add optimistic UI updates and error toast boundaries",
                    ],
                )
            )
            assignments.append(
                TeamMemberAssignment(
                    teammate_name=names[1],
                    assigned_role="Backend API & Cloud Operations Lead",
                    assigned_layers=["Backend FastAPI", "Redis Topology", "Docker / AWS"],
                    companion_robot=TRANSFORMERS_ROBOTS["ironhide"],
                    git_branch="feat/backend-api-infra",
                    custom_ide_prompt=(
                        "Lead Backend with Ironhide. Build async FastAPI routes with ResponseEnvelope[T], "
                        "Redis caching and distributed locks, and Docker multi-stage build."
                    ),
                    starter_checklist=[
                        "Expose REST endpoints with Pydantic v2 schemas",
                        "Implement circuit breakers and idempotency locks",
                        "Write automated pytest test suite",
                    ],
                )
            )
            assignments.append(
                TeamMemberAssignment(
                    teammate_name=names[2],
                    assigned_role="AI Multi-Agent & Database Lead",
                    assigned_layers=["LangGraph Agents", "FastMCP Tools", "PostgreSQL pgvector"],
                    companion_robot=TRANSFORMERS_ROBOTS["wheeljack"],
                    git_branch="feat/ai-agents-data",
                    custom_ide_prompt=(
                        "Lead AI & Data with Wheeljack & Ratchet. Construct cyclic LangGraph workflows, "
                        "pgvector HNSW hybrid retrieval, and FastMCP server tools."
                    ),
                    starter_checklist=[
                        "Implement LangGraph nodes and conditional router",
                        "Tune FlashRank neural reranker top_k=5",
                        "Apply Supabase RLS security policies",
                    ],
                )
            )

        elif team_size == 4:
            names = [
                provided_profiles[i].name
                if provided_profiles and len(provided_profiles) > i
                else f"Teammate {i + 1}"
                for i in range(4)
            ]
            roles = [
                (
                    "Frontend Lead",
                    ["Frontend UI"],
                    TRANSFORMERS_ROBOTS["mirage"],
                    "feat/frontend-ui",
                ),
                (
                    "Backend API Lead",
                    ["Backend FastAPI", "Redis"],
                    TRANSFORMERS_ROBOTS["ironhide"],
                    "feat/backend-api",
                ),
                (
                    "AI Systems Lead",
                    ["LangGraph", "FastMCP", "Reranker"],
                    TRANSFORMERS_ROBOTS["wheeljack"],
                    "feat/ai-engine",
                ),
                (
                    "Data & Cloud Lead",
                    ["PostgreSQL pgvector", "Docker", "DevOps"],
                    TRANSFORMERS_ROBOTS["ratchet"],
                    "feat/database-cloud",
                ),
            ]
            for i, (role, layers, bot, branch) in enumerate(roles):
                assignments.append(
                    TeamMemberAssignment(
                        teammate_name=names[i],
                        assigned_role=role,
                        assigned_layers=layers,
                        companion_robot=bot,
                        git_branch=branch,
                        custom_ide_prompt=f"Role: {role}. Partner Autobot: {bot.codename}. Problem: {problem_statement}. Strict quality gates.",
                        starter_checklist=[
                            f"Initialize {branch} branch",
                            f"Review {bot.assigned_skills[0]} best practices",
                            "Ensure 100% test pass rate",
                        ],
                    )
                )

        else:  # 5 or 6+
            names = [
                provided_profiles[i].name
                if provided_profiles and len(provided_profiles) > i
                else f"Teammate {i + 1}"
                for i in range(min(team_size, 6))
            ]
            standard_5 = [
                (
                    "Frontend & UX Lead",
                    ["Frontend UI & Aesthetics"],
                    TRANSFORMERS_ROBOTS["mirage"],
                    "feat/frontend",
                ),
                (
                    "Backend & Resilience Lead",
                    ["FastAPI & Redis"],
                    TRANSFORMERS_ROBOTS["ironhide"],
                    "feat/backend",
                ),
                (
                    "AI & Multi-Agent Lead",
                    ["LangGraph & FastMCP"],
                    TRANSFORMERS_ROBOTS["wheeljack"],
                    "feat/ai-agents",
                ),
                (
                    "Database & Security Lead",
                    ["PostgreSQL pgvector & RLS"],
                    TRANSFORMERS_ROBOTS["ratchet"],
                    "feat/database",
                ),
                (
                    "Cloud DevOps & Stage Scout",
                    ["Docker, AWS & Pitch Deck"],
                    TRANSFORMERS_ROBOTS["bumblebee"],
                    "feat/devops-pitch",
                ),
            ]
            for i in range(5):
                role, layers, bot, branch = standard_5[i]
                assignments.append(
                    TeamMemberAssignment(
                        teammate_name=names[i],
                        assigned_role=role,
                        assigned_layers=layers,
                        companion_robot=bot,
                        git_branch=branch,
                        custom_ide_prompt=f"Role: {role}. Partner Autobot: {bot.codename}. Focus on your layer: {', '.join(layers)}.",
                        starter_checklist=[
                            f"Checkout branch {branch}",
                            f"Verify {bot.codename} assigned skills",
                            "Build modular components",
                        ],
                    )
                )
            if team_size >= 6:
                for i in range(5, team_size):
                    extra_name = (
                        provided_profiles[i].name
                        if provided_profiles and len(provided_profiles) > i
                        else f"Teammate {i + 1}"
                    )
                    assignments.append(
                        TeamMemberAssignment(
                            teammate_name=extra_name,
                            assigned_role="QA, Benchmark & Evaluation Specialist",
                            assigned_layers=[
                                "RAGAS Eval Harness",
                                "Load Testing",
                                "Live Presentation",
                            ],
                            companion_robot=TRANSFORMERS_ROBOTS["orbit_prime"],
                            git_branch=f"feat/eval-benchmarks-{i + 1}",
                            custom_ide_prompt="Execute automated RAGAS eval tests, load testing scripts, and pitch script rehearsal.",
                            starter_checklist=[
                                "Run pytest test suite",
                                "Validate P95 response times < 200ms",
                                "Verify offline demo.sh fallback",
                            ],
                        )
                    )

        return assignments

    def generate_features_menu(
        self,
        problem_statement: str,
        domain: str,
        aesthetic: FrontendAestheticDecision,
    ) -> FullSystemFeaturesMenu:
        """
        Synthesizes a comprehensive, actionable Features Menu across all 5 technical layers
        customized specifically to the hackathon problem statement.
        """
        slug = re.sub(r"[^a-zA-Z0-9]+", "_", domain.lower()).strip("_")

        # 1. Frontend Menu
        frontend_menu = LayerFeaturesMenu(
            layer_name="Frontend UI & Visual Experience",
            executive_summary=(
                f"High-fidelity responsive interface crafted with {aesthetic.aesthetic_name} visual paradigm. "
                f"Features zero layout shifts, accessible contrast, and smooth micro-interactions."
            ),
            core_features=[
                {
                    "name": "Live Mission Control & Studio Dashboard",
                    "description": "Primary interactive screen with telemetry feeds, search inputs, and job controls.",
                    "status": "Ready in HSF",
                    "path": "/dashboard",
                },
                {
                    "name": "Streaming Job Execution Monitor",
                    "description": "Server-Sent Events (SSE) subscriber rendering real-time token streams & progress logs.",
                    "status": "Ready in HSF",
                    "path": "/jobs/:id/stream",
                },
                {
                    "name": "Human-in-the-Loop Review Intercept Modal",
                    "description": "Accessible dialog that pauses automated workflows to require explicit human sign-off.",
                    "status": "Ready in HSF",
                    "path": "/components/HumanApprovalModal.tsx",
                },
                {
                    "name": "Aesthetic Design System Switcher",
                    "description": "Dynamic CSS token runtime supporting Skeuomorphism, Claymorphism, Glassmorphism, Neo-Brutalism, and Industrial Brutalism.",
                    "status": "Ready in HSF",
                    "path": "/components/AestheticSwitcher.tsx",
                },
            ],
            recommended_libraries=[
                "Next.js 14 App Router",
                "Tailwind CSS v3.4",
                "Framer Motion",
                "Lucide React",
            ],
            performance_budget="First Contentful Paint < 0.8s, Zero Cumulative Layout Shift (CLS = 0)",
            security_and_compliance="Strict CSP headers, XSS sanitization via DOMPurify",
        )

        # 2. Backend Menu
        backend_menu = LayerFeaturesMenu(
            layer_name="Backend API & Middleware",
            executive_summary=(
                "High-performance asynchronous FastAPI microservice with ResponseEnvelope[T], "
                "Redis-backed sliding-window rate limiting, and resilient circuit breaker states."
            ),
            core_features=[
                {
                    "name": "Ingestion & Embedding Pipeline API",
                    "route": f"POST /api/v1/{slug}/ingest",
                    "description": "Chunking, metadata tagging, and vector generation with SHA-256 deduplication.",
                },
                {
                    "name": "Hybrid RRF Query Retrieval Endpoint",
                    "route": f"POST /api/v1/{slug}/query",
                    "description": "Reciprocal Rank Fusion (k=60) combining dense vector search and sparse BM25 text rank.",
                },
                {
                    "name": "Real-time SSE Job Streamer",
                    "route": f"GET /api/v1/{slug}/jobs/{{id}}/stream",
                    "description": "Pub/Sub bridge streaming progress tokens directly to web clients.",
                },
                {
                    "name": "Circuit Breaker Telemetry Monitor",
                    "route": "/api/v1/health/circuit-breakers",
                    "description": "Exposes real-time circuit state (CLOSED, OPEN, HALF_OPEN) with failure counters.",
                },
            ],
            recommended_libraries=[
                "FastAPI 0.115+",
                "Uvicorn (Standard)",
                "Pydantic v2",
                "httpx (AsyncClient)",
                "redis-py (ConnectionPool)",
            ],
            performance_budget="P95 API response time < 85ms, P99 < 180ms",
            security_and_compliance="JWT Bearer Authentication, distributed SETNX idempotency locks, CORS whitelist",
        )

        # 3. Database Menu
        database_menu = LayerFeaturesMenu(
            layer_name="Database & Vector Storage",
            executive_summary=(
                "PostgreSQL 16 relational engine equipped with pgvector extension, "
                "HNSW cosine index, TSVECTOR full-text search, and Supabase Row-Level Security."
            ),
            core_features=[
                {
                    "table_name": f"{slug}_documents",
                    "type": "Relational Entity",
                    "indexes": ["id (PK, UUID)", "created_at (DESC)", "tenant_id (BTREE)"],
                    "description": "Stores master document metadata, tenant ownership, and status flags.",
                },
                {
                    "table_name": f"{slug}_chunks",
                    "type": "Vector Embedding & Full-Text Search",
                    "indexes": [
                        "embedding (HNSW vector_cosine_ops, m=16, ef_construction=64)",
                        "tsv_content (GIN tsvector)",
                    ],
                    "description": "Contains split text chunks with 1536-dimensional embeddings for hybrid retrieval.",
                },
                {
                    "table_name": f"{slug}_audit_trail",
                    "type": "Immutable Compliance Log",
                    "indexes": ["id (PK)", "timestamp (DESC)", "action_type (BTREE)"],
                    "description": "Immutable log of all user operations and agentic decisions for judge auditability.",
                },
            ],
            recommended_libraries=[
                "PostgreSQL 16",
                "pgvector",
                "asyncpg",
                "SQLAlchemy 2.0 (AsyncEngine)",
                "Alembic",
            ],
            performance_budget="HNSW vector retrieval < 12ms over 100,000 vectors",
            security_and_compliance="Supabase Row-Level Security (RLS) policies, SSL encrypted connection pools",
        )

        # 4. AI & Multi-Agent Menu
        ai_menu = LayerFeaturesMenu(
            layer_name="AI & Multi-Agent Cognitive Engine",
            executive_summary=(
                "LangGraph stateful multi-agent supervisor graph coordinating specialist worker nodes, "
                "FastMCP tool servers over SSE, and FlashRank neural rerankers with RAGAS evaluation."
            ),
            core_features=[
                {
                    "name": "Cyclic LangGraph Supervisor State Machine",
                    "nodes": [
                        "ParserNode",
                        "RetrieverNode",
                        "RerankerNode",
                        "WorkerNode",
                        "HumanGateNode",
                    ],
                    "description": "StateGraph with checkpointing that handles complex multi-step reasoning cycles.",
                },
                {
                    "name": "FlashRank Sub-20ms Neural Reranker",
                    "model": "ms-marco-TinyBERT-L-2-v2",
                    "description": "Neural cross-encoder reranking 25 retrieved candidates to top 5 in <18ms on CPU.",
                },
                {
                    "name": "FastMCP Server Tools",
                    "protocol": "Model Context Protocol (JSON-RPC over SSE)",
                    "description": "Exposes database search, calculations, and domain tools to LLMs safely.",
                },
                {
                    "name": "Automated RAGAS Evaluation Harness",
                    "metrics": ["Faithfulness", "Answer Relevancy", "Context Precision"],
                    "description": "CI test gate verifying output quality and blocking hallucinations.",
                },
            ],
            recommended_libraries=[
                "LangGraph 0.2+",
                "LangChain Core",
                "FastMCP",
                "FlashRank",
                "ragas",
            ],
            performance_budget="Total agent reasoning cycle < 1.8s (including rerank & synthesis)",
            security_and_compliance="Input guardrails blocking prompt injection, Human interrupt gate on DB writes",
        )

        # 5. DevOps & Cloud Menu
        devops_menu = LayerFeaturesMenu(
            layer_name="Cloud DevOps & Stage Deployment",
            executive_summary=(
                "Multi-stage Docker containers (<180MB), automated GitHub Actions CI, "
                "AWS ECS Fargate serverless task definitions, and offline demo.sh presentation fail-safe."
            ),
            core_features=[
                {
                    "name": "Multi-Stage Dockerfile",
                    "size_target": "<180MB uncompressed",
                    "description": "Alpine/Slim Python 3.11 base with non-root security user and cached wheels.",
                },
                {
                    "name": "Docker Compose Local Topology",
                    "services": [
                        "app (FastAPI)",
                        "postgres (pgvector)",
                        "redis",
                        "dashboard (Next.js)",
                    ],
                    "description": "Single-command local environment launch: docker compose up -d.",
                },
                {
                    "name": "AWS ECS Fargate Task Definition",
                    "specs": "0.5 vCPU / 1GB RAM, auto-scaling to 4 tasks",
                    "description": "Zero-server maintenance production deployment with CloudWatch logs.",
                },
                {
                    "name": "Stage Fail-Safe Demo Script (demo.sh)",
                    "resilience": "100% Offline Capable",
                    "description": "Pre-cached mock data script guaranteeing flawless live demo even if venue Wi-Fi drops.",
                },
            ],
            recommended_libraries=[
                "Docker 26+",
                "Docker Compose v2",
                "GitHub Actions",
                "AWS ECS Fargate",
                "Marp Presentation Engine",
            ],
            performance_budget="CI build time < 2.5 minutes, Container startup time < 4.2 seconds",
            security_and_compliance="Non-root container user, zero environment variables checked into git, pinned SHA hashes",
        )

        return FullSystemFeaturesMenu(
            problem_statement=problem_statement,
            domain=domain,
            frontend_menu=frontend_menu,
            backend_menu=backend_menu,
            database_menu=database_menu,
            ai_agentic_menu=ai_menu,
            devops_cloud_menu=devops_menu,
        )
