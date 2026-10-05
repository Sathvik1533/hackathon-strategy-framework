"""
Orbit: The Hackathon Strategy Mascot & Autonomous Problem Decomposer
(ai_layer/mascot_agent.py)

Autonomous internal agent that ingests any hackathon problem statement,
deconstructs requirements, maps them strictly onto our pre-ready tech stack,
selects the exact tools and skills to activate, provides competitive moat analysis,
and generates ready-made boilerplate prompts for Antigravity, Claude, Cursor, and Hero agents.
"""

from __future__ import annotations

import re
import sys
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


class MascotStrategyPlan(BaseModel):
    mascot_name: str = "Orbit 🤖🚀"
    problem_statement: str
    domain_classified: str
    executive_strategy: str
    competitive_advantage_vs_peers: List[str]
    skills_activated: List[str]
    tech_stack_mapping: TechStackMapping
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

        return MascotStrategyPlan(
            mascot_name=self.name,
            problem_statement=cleaned_problem,
            domain_classified=detected_domain,
            executive_strategy=(
                f"Orbit has analyzed '{cleaned_problem}'! We will conquer this domain by mapping its data flows "
                f"directly into our 7-layer HSF architecture. We will leverage PostgreSQL pgvector for hybrid retrieval, "
                f"LangGraph for multi-agent reasoning with a human-in-the-loop safety gate, Redis for sub-10ms semantic caching, "
                f"and present an interactive Archify blueprint backed by verified RAGAS faithfulness metrics."
            ),
            competitive_advantage_vs_peers=competitive_moats,
            skills_activated=skills_activated,
            tech_stack_mapping=tech_mapping,
            teammate_prompts=prompts,
            stage_pitch_hook=stage_hook,
            estimated_setup_time_minutes=1,
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
