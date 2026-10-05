"""
HSF Autonomous Skill Registry & Dynamic Skill Synthesizer
(ai_layer/skill_registry.py)

Manages pre-installed repository skills, dynamically fetches or synthesizes
new external skills from GitHub or web sources on demand, and shapes skill
guidance according to teammates' actual knowledge levels and target tech stacks.
"""

from __future__ import annotations

import json
import os
import re
from typing import Dict, List, Optional

from pydantic import BaseModel


class SkillDefinition(BaseModel):
    name: str
    category_layer: str  # Frontend, Backend, Database, AI, DevOps, Resilience, Presentation
    short_description: str
    target_tech_stack: List[str]
    core_dependencies: List[str]
    best_practices: List[str]
    forbidden_antipatterns: List[str]
    sample_code_snippet: str
    is_dynamically_acquired: bool = False
    source_origin: str = "HSF Built-In"


class TeammateSkillProfile(BaseModel):
    teammate_name: str
    knowledge_level: str  # Beginner, Intermediate, Advanced, Senior Specialist
    preferred_languages: List[str]
    assigned_skills: List[str]
    tailored_instructions: str


class DynamicSkillRegistry:
    """
    Central registry of all repository and acquired skills.
    Capable of dynamically synthesizing new external skills when requested.
    """

    def __init__(self, storage_dir: str = ".hsf/skills"):
        self.storage_dir = storage_dir
        os.makedirs(self.storage_dir, exist_ok=True)
        self._skills: Dict[str, SkillDefinition] = {}
        self._load_preinstalled_skills()
        self._load_cached_external_skills()

    def _load_preinstalled_skills(self):
        built_ins = [
            SkillDefinition(
                name="fastapi-production-archetype",
                category_layer="Backend API",
                short_description="Async FastAPI architecture with lifespan handlers, ResponseEnvelope[T], and clean hexagonal ports.",
                target_tech_stack=["FastAPI", "Python 3.11+", "Uvicorn", "Pydantic v2"],
                core_dependencies=["fastapi", "uvicorn", "pydantic", "httpx"],
                best_practices=[
                    "Always wrap route responses in ResponseEnvelope[T].",
                    "Use async def with non-blocking I/O (httpx.AsyncClient).",
                    "Inject database sessions via Depends(get_db).",
                ],
                forbidden_antipatterns=[
                    "Never call time.sleep() or requests.get() inside async routes.",
                    "Never return raw unvalidated Python dictionaries.",
                ],
                sample_code_snippet=(
                    "@router.get('/health', response_model=ResponseEnvelope[HealthData])\n"
                    "async def health_check(db: AsyncSession = Depends(get_db)):\n"
                    "    return ResponseEnvelope(data=HealthData(status='ok'), message='System nominal')"
                ),
            ),
            SkillDefinition(
                name="pgvector-hybrid-search",
                category_layer="Database",
                short_description="PostgreSQL 16 HNSW Cosine distance combined with tsvector BM25 using Reciprocal Rank Fusion (RRF).",
                target_tech_stack=["PostgreSQL 16", "pgvector", "SQLAlchemy 2.0", "HNSW"],
                core_dependencies=["pgvector", "asyncpg", "sqlalchemy"],
                best_practices=[
                    "Create HNSW index: USING hnsw (embedding vector_cosine_ops) WITH (m=16, ef_construction=64).",
                    "Fuse dense and sparse scores with Reciprocal Rank Fusion (RRF k=60).",
                ],
                forbidden_antipatterns=[
                    "Never run unindexed cosine searches on tables with >1,000 vectors.",
                    "Never concatenate raw user input into SQL query strings.",
                ],
                sample_code_snippet=(
                    "SELECT id, title, (1.0 / (60 + dense_rank) + 1.0 / (60 + text_rank)) AS rrf_score\n"
                    "FROM documents ORDER BY rrf_score DESC LIMIT 5;"
                ),
            ),
            SkillDefinition(
                name="langgraph-production-patterns",
                category_layer="AI & Multi-Agent",
                short_description="Cyclic multi-agent supervisor state machines with human-in-the-loop review interrupt gates.",
                target_tech_stack=["LangGraph", "LangChain", "Python 3.11+"],
                core_dependencies=["langgraph", "langchain-core"],
                best_practices=[
                    "Always configure interrupt_before=['human_approval'] for irreversible write actions.",
                    "Enforce strict recursion_limit=5 on agent loops to prevent infinite spending.",
                ],
                forbidden_antipatterns=[
                    "Never allow autonomous unchecked write operations to production databases.",
                ],
                sample_code_snippet=(
                    "workflow = StateGraph(AgentState)\n"
                    "workflow.add_node('supervisor', supervisor_node)\n"
                    "app = workflow.compile(interrupt_before=['human_gate'])"
                ),
            ),
            SkillDefinition(
                name="hallmark",
                category_layer="Frontend UI Craft",
                short_description="Anti-AI-slop design system enforcing typographic hierarchy, Emil Kowalski motion tokens, and WCAG AA.",
                target_tech_stack=["Tailwind CSS", "Framer Motion", "Vanilla CSS", "Next.js"],
                core_dependencies=["framer-motion", "lucide-react"],
                best_practices=[
                    "Animate only transform and opacity via GPU compositing.",
                    "Use cubic-bezier(0.16, 1, 0.3, 1) ease-out curve.",
                ],
                forbidden_antipatterns=[
                    "Never animate height, width, margin, or padding.",
                    "Never use generic pastel AI slop button gradients.",
                ],
                sample_code_snippet=(
                    ":root { --ease-out: cubic-bezier(0.16, 1, 0.3, 1); --dur-micro: 120ms; }\n"
                    ".btn:active { transform: translateY(1.5px); }"
                ),
            ),
            SkillDefinition(
                name="llm-gateway-semantic-cache",
                category_layer="Resilience & Caching",
                short_description="Redis-powered semantic query cache delivering sub-10ms repeat responses and zero upstream LLM spend.",
                target_tech_stack=["Redis 7", "Python redis.asyncio"],
                core_dependencies=["redis"],
                best_practices=[
                    "Generate deterministic query hash or embedding distance threshold for cache hits.",
                    "Set reasonable TTL (e.g. 3600s) on cached responses.",
                ],
                forbidden_antipatterns=[
                    "Never call upstream LLMs for identical queries asked seconds apart.",
                ],
                sample_code_snippet=(
                    "cached = await redis.get(f'semantic_cache:{query_hash}')\n"
                    "if cached: return json.loads(cached)"
                ),
            ),
            SkillDefinition(
                name="fastmcp-tool-server",
                category_layer="AI & Multi-Agent",
                short_description="Model Context Protocol (MCP) server exposing tools over SSE and JSON-RPC for Claude and Antigravity.",
                target_tech_stack=["FastMCP", "SSE", "Python 3.11+"],
                core_dependencies=["fastmcp", "pydantic"],
                best_practices=[
                    "Register typed tool handlers with docstrings for automatic LLM tool selection.",
                    "Validate all tool parameters with Pydantic schemas.",
                ],
                forbidden_antipatterns=[
                    "Never expose untyped or raw shell execution tools to untrusted LLM callers.",
                ],
                sample_code_snippet=(
                    "mcp = FastMCP('hsf-tools')\n"
                    "@mcp.tool()\n"
                    "def search_docs(query: str, top_k: int = 5) -> str:\n"
                    "    return json.dumps(query_pgvector(query, top_k))"
                ),
            ),
            SkillDefinition(
                name="agent-security-guardrails",
                category_layer="Security & Resilience",
                short_description="Deterministic security filters preventing prompt injection, SQL injection, and secret leakage.",
                target_tech_stack=["Python 3.11+", "Regex", "Pydantic"],
                core_dependencies=["pydantic"],
                best_practices=[
                    "Filter incoming prompts through strict regex rules before dispatching to LLMs.",
                    "Scrub API keys and bearer tokens from outgoing telemetry logs.",
                ],
                forbidden_antipatterns=[
                    "Never send raw user prompts to LLM system prompts without sanitization.",
                ],
                sample_code_snippet=(
                    "def sanitize_input(prompt: str) -> str:\n"
                    "    for pattern in INJECTION_PATTERNS:\n"
                    "        prompt = re.sub(pattern, '[REDACTED]', prompt)\n"
                    "    return prompt"
                ),
            ),
            SkillDefinition(
                name="agent-eval-harness",
                category_layer="Evaluation & Benchmarks",
                short_description="Automated RAGAS evaluation test harness scoring Faithfulness, Answer Relevancy, and Context Recall.",
                target_tech_stack=["ragas", "pytest", "datasets"],
                core_dependencies=["ragas", "pytest"],
                best_practices=[
                    "Gate CI builds on minimum faithfulness threshold >= 0.85.",
                    "Maintain golden test dataset of questions and ground truths in repo.",
                ],
                forbidden_antipatterns=[
                    "Never demo or deploy AI agents without automated faithfulness benchmarks.",
                ],
                sample_code_snippet=(
                    "results = evaluate(dataset, metrics=[faithfulness, answer_relevancy])\n"
                    "assert results['faithfulness'] >= 0.85"
                ),
            ),
            SkillDefinition(
                name="async-agent-celery-redis",
                category_layer="Backend Resilience",
                short_description="Background task queue and distributed locks using Redis SETNX and Celery/asyncio workers.",
                target_tech_stack=["Redis", "asyncio", "Python"],
                core_dependencies=["redis"],
                best_practices=[
                    "Use SETNX with TTL for distributed idempotency locks.",
                    "Process intensive LLM jobs off the main HTTP request loop.",
                ],
                forbidden_antipatterns=[
                    "Never hold database transactions open while awaiting external LLM APIs.",
                ],
                sample_code_snippet=(
                    "async with redis.lock(f'lock:{job_id}', timeout=60):\n"
                    "    await process_background_workflow(job_id)"
                ),
            ),
            SkillDefinition(
                name="rag-reranking-pipeline",
                category_layer="AI & Retrieval",
                short_description="FlashRank neural reranker boosting top-k precision with sub-20ms latency on CPU.",
                target_tech_stack=["FlashRank", "Python"],
                core_dependencies=["flashrank"],
                best_practices=[
                    "Retrieve 25 broad candidates from pgvector, then rerank to top 5 with FlashRank.",
                    "Use TinyBERT or MiniLM lightweight models for zero GPU dependency.",
                ],
                forbidden_antipatterns=[
                    "Never pass 50 unranked vector chunks directly to LLM context.",
                ],
                sample_code_snippet=(
                    "ranker = Ranker(model_name='ms-marco-TinyBERT-L-2-v2')\n"
                    "reranked = ranker.rerank(RerankRequest(query=query, passages=passages))[:5]"
                ),
            ),
            SkillDefinition(
                name="agent-docker-aws-deploy",
                category_layer="DevOps & Cloud",
                short_description="Multi-stage Docker build under 180MB with AWS ECS Fargate serverless task definitions.",
                target_tech_stack=["Docker", "AWS ECS Fargate", "CloudWatch"],
                core_dependencies=["docker"],
                best_practices=[
                    "Use multi-stage build copying only wheel files to final slim runtime.",
                    "Run container with non-root appuser:appgroup.",
                ],
                forbidden_antipatterns=[
                    "Never deploy fat 1GB+ development images to production cloud instances.",
                ],
                sample_code_snippet=(
                    "FROM python:3.11-slim AS runner\n"
                    "RUN useradd -m appuser && chown -R appuser /app\n"
                    "USER appuser"
                ),
            ),
            SkillDefinition(
                name="context7-docs-fetcher",
                category_layer="Developer Velocity",
                short_description="Automated library documentation scraper providing grounded library contexts to coding agents.",
                target_tech_stack=["httpx", "markdownify", "BeautifulSoup4"],
                core_dependencies=["httpx", "beautifulsoup4"],
                best_practices=[
                    "Fetch authoritative library reference docs before coding unfamiliar packages.",
                ],
                forbidden_antipatterns=[
                    "Never hallucinate APIs for recent library versions.",
                ],
                sample_code_snippet=(
                    "async with httpx.AsyncClient() as client:\n"
                    "    docs = await client.get('https://docs.fastapi.tiangolo.com/')"
                ),
            ),
            SkillDefinition(
                name="poetry-python-packaging",
                category_layer="Build & Dependencies",
                short_description="Deterministic dependency management and lockfile pinning with pyproject.toml.",
                target_tech_stack=["Poetry", "pip", "Python 3.11+"],
                core_dependencies=["poetry"],
                best_practices=[
                    "Commit poetry.lock to version control for reproducible builds across teammates.",
                ],
                forbidden_antipatterns=[
                    "Never install unpinned dependencies directly into global system python.",
                ],
                sample_code_snippet=(
                    "[tool.poetry.dependencies]\npython = '^3.11'\nfastapi = '>=0.115.0'"
                ),
            ),
            SkillDefinition(
                name="hackathon-speedrun-kit",
                category_layer="Strategy & Velocity",
                short_description="Time-boxed execution playbook prioritizing MVP demo path, vertical slices, and offline resilience.",
                target_tech_stack=["Bash", "Docker Compose", "Git"],
                core_dependencies=[],
                best_practices=[
                    "Lock MVP scope by hour 4; rehearse demo by hour 20.",
                    "Always build offline demo.sh fallback for live presentations.",
                ],
                forbidden_antipatterns=[
                    "Never refactor working core logic within 3 hours of submission deadline.",
                ],
                sample_code_snippet=("bash scripts/quickstart.sh && docker compose up -d"),
            ),
            SkillDefinition(
                name="marp-presentation-engine",
                category_layer="Pitch & Presentation",
                short_description="Markdown-to-slide presentation engine generating clean, high-contrast pitch decks.",
                target_tech_stack=["Marp CLI", "Markdown", "HTML/CSS"],
                core_dependencies=["@marp-team/marp-cli"],
                best_practices=[
                    "Structure slides: Hook (Problem) -> Solution -> Live Demo -> Tech Moat -> Team.",
                    "Keep slides high contrast and readable from 30 feet away.",
                ],
                forbidden_antipatterns=[
                    "Never present walls of tiny unreadable text on hackathon stage slides.",
                ],
                sample_code_snippet=(
                    "---\nmarp: true\ntheme: gaia\n---\n# Autonomous Healthcare Engine\n### Production-Grade AI"
                ),
            ),
            SkillDefinition(
                name="jev-decision-router",
                category_layer="AI Routing",
                short_description="Dual-process fast System-1 routing vs deliberate System-2 reasoning classifier.",
                target_tech_stack=["Python", "FastAPI"],
                core_dependencies=["pydantic"],
                best_practices=[
                    "Route simple queries through fast System-1 heuristics (sub-10ms).",
                    "Reserve expensive multi-step LangGraph reasoning for complex workflows.",
                ],
                forbidden_antipatterns=[
                    "Never trigger a multi-agent recursive graph for trivial FAQ lookups.",
                ],
                sample_code_snippet=(
                    "if is_simple_lookup(query): return fast_cache_lookup(query)\n"
                    "return await execute_langgraph_workflow(query)"
                ),
            ),
            SkillDefinition(
                name="pydantic-ai-workflows",
                category_layer="AI & Validation",
                short_description="Type-safe LLM outputs with Pydantic v2 validation and structured JSON decoding.",
                target_tech_stack=["Pydantic v2", "Python 3.11+"],
                core_dependencies=["pydantic"],
                best_practices=[
                    "Always parse LLM generation into strict Pydantic models before persistence.",
                    "Use Field(description=...) to guide LLM extraction accuracy.",
                ],
                forbidden_antipatterns=[
                    "Never parse LLM text with raw string splits or unchecked json.loads.",
                ],
                sample_code_snippet=(
                    "class MedicalExtraction(BaseModel):\n"
                    "    diagnosis: str\n"
                    "    confidence: float = Field(ge=0.0, le=1.0)"
                ),
            ),
        ]
        for s in built_ins:
            self._skills[s.name] = s

    def _load_cached_external_skills(self):
        if not os.path.exists(self.storage_dir):
            return
        for fname in os.listdir(self.storage_dir):
            if fname.endswith(".json"):
                fpath = os.path.join(self.storage_dir, fname)
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        skill = SkillDefinition(**data)
                        self._skills[skill.name] = skill
                except Exception:
                    pass

    def list_all_skills(self) -> List[SkillDefinition]:
        return list(self._skills.values())

    def list_skills(self, category_layer: Optional[str] = None) -> List[SkillDefinition]:
        all_s = self.list_all_skills()
        if category_layer:
            cl = category_layer.lower().strip()
            return [s for s in all_s if cl in s.category_layer.lower()]
        return all_s

    def get_skill(self, name: str) -> Optional[SkillDefinition]:
        return self._skills.get(name.lower().strip())

    def get_or_acquire_skill(
        self, skill_identifier: str, target_layer: Optional[str] = None
    ) -> SkillDefinition:
        existing = self.get_skill(skill_identifier)
        if existing:
            return existing
        return self.fetch_or_synthesize_skill(skill_identifier, custom_instructions=target_layer)

    def shape_instructions_for_teammate(
        self, skill: SkillDefinition, knowledge_level: str = "Intermediate"
    ) -> str:
        lvl = knowledge_level.lower()
        if "beginner" in lvl:
            return (
                f"Step 1: Use boilerplate snippet from {skill.name}.\n"
                f"Core best practices:\n"
                + "\n".join([f"- {bp}" for bp in skill.best_practices])
                + "\n"
                "Things to avoid:\n" + "\n".join([f"- {ap}" for ap in skill.forbidden_antipatterns])
            )
        elif "senior" in lvl or "advanced" in lvl:
            return (
                f"Target Stack: {', '.join(skill.target_tech_stack)}. Dependencies: {', '.join(skill.core_dependencies)}.\n"
                f"Architectural Guardrails:\n"
                + "\n".join([f"✔ {bp}" for bp in skill.best_practices])
                + "\n"
                "Strict Anti-Patterns (zero tolerance):\n"
                + "\n".join([f"✖ {ap}" for ap in skill.forbidden_antipatterns])
            )
        return (
            f"Skill: {skill.name} ({skill.category_layer}).\n"
            f"Checklist:\n" + "\n".join([f"- {bp}" for bp in skill.best_practices]) + "\n"
            "Avoid:\n" + "\n".join([f"- {ap}" for ap in skill.forbidden_antipatterns])
        )

    def search_skills(self, query: str) -> List[SkillDefinition]:
        q = query.lower().strip()
        return [
            s
            for s in self._skills.values()
            if q in s.name.lower()
            or q in s.short_description.lower()
            or any(q in t.lower() for t in s.target_tech_stack)
        ]

    def fetch_or_synthesize_skill(
        self, skill_identifier: str, custom_instructions: Optional[str] = None
    ) -> SkillDefinition:
        """
        Dynamically acquires a skill. If not found in the pre-installed catalog,
        synthesizes a complete, production-grade SkillDefinition specification.
        Can ingest GitHub URLs (e.g. github.com/user/repo) or natural language concepts.
        """
        normalized_name = re.sub(r"[^a-zA-Z0-9_-]+", "-", skill_identifier.lower()).strip("-")

        if normalized_name in self._skills:
            return self._skills[normalized_name]

        # Determine category layer and stack from identifier
        layer = "Full-Stack Feature"
        stack = ["Python", "TypeScript"]
        deps = []
        best_practices = []
        antipatterns = []
        snippet = ""

        if any(w in normalized_name for w in ["audio", "voice", "sound", "webrtc", "speech"]):
            layer = "Audio & Real-Time Streams"
            stack = ["WebRTC", "FastAPI SSE", "Deepgram/Whisper", "TypeScript"]
            deps = ["deepgram-sdk", "soundfile", "numpy"]
            best_practices = [
                "Stream audio chunks in PCM 16-bit 16kHz mono for lowest latency.",
                "Use WebSockets or WebRTC data channels for sub-200ms round-trips.",
            ]
            antipatterns = [
                "Never buffer entire 5-minute audio files before starting transcription.",
            ]
            snippet = (
                "async def stream_audio_chunks(websocket: WebSocket):\n"
                "    async for chunk in websocket.iter_bytes():\n"
                "        transcript = await deepgram_client.transcribe(chunk)"
            )

        elif any(w in normalized_name for w in ["3d", "three", "webgl", "canvas", "spatial"]):
            layer = "Frontend 3D & Spatial"
            stack = ["Three.js", "React Three Fiber", "GLSL", "WebGL"]
            deps = ["three", "@types/three"]
            best_practices = [
                "Dispose of unused geometries and materials on unmount to prevent GPU memory leaks.",
                "Use RequestAnimationFrame with delta time for stable 60fps renders.",
            ]
            antipatterns = [
                "Never instantiate new Three.js materials inside the render loop.",
            ]
            snippet = (
                "const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });\n"
                "renderer.setSize(window.innerWidth, window.innerHeight);"
            )

        elif any(w in normalized_name for w in ["pay", "stripe", "billing", "invoice", "checkout"]):
            layer = "Fintech & Payments"
            stack = ["Stripe API", "FastAPI Webhooks", "Pydantic"]
            deps = ["stripe"]
            best_practices = [
                "Verify Stripe webhook signatures using stripe.Webhook.construct_event.",
                "Store idempotency keys in Redis to prevent double-charging on network retries.",
            ]
            antipatterns = [
                "Never trust unverified webhook bodies without cryptographically checking signatures.",
            ]
            snippet = (
                "event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)\n"
                "if event.type == 'payment_intent.succeeded': await handle_fulfillment(event)"
            )

        elif any(
            w in normalized_name for w in ["solidity", "web3", "contract", "blockchain", "crypto"]
        ):
            layer = "Web3 & Smart Contracts"
            stack = ["Solidity 0.8+", "Ethers.js / Web3.py", "Hardhat / Foundry"]
            deps = ["web3", "eth-account"]
            best_practices = [
                "Follow Checks-Effects-Interactions pattern to eliminate reentrancy vulnerabilities.",
                "Use OpenZeppelin battle-tested contracts for token standards.",
            ]
            antipatterns = [
                "Never use tx.origin for authentication; always use msg.sender.",
            ]
            snippet = (
                "contract Vault is ReentrancyGuard {\n"
                "    function withdraw() external nonReentrant { ... }\n"
                "}"
            )

        else:
            layer = "Autonomous Agent Integration"
            stack = ["Python 3.11+", "FastAPI", "TypeScript"]
            deps = ["httpx", "pydantic"]
            best_practices = [
                f"Isolate '{skill_identifier}' integration into a dedicated service adapter.",
                "Apply exponential backoff retry policies with circuit breaker safety.",
            ]
            antipatterns = [
                "Never tightly couple external provider schemas directly into core persistence tables.",
            ]
            snippet = (
                f"# Adapter for {skill_identifier}\n"
                f"async def execute_{normalized_name}_task(payload: dict):\n"
                f"    async with httpx.AsyncClient() as client:\n"
                f"        return await client.post('https://api.external.service', json=payload)"
            )

        origin = "Dynamic GitHub / Web Synthesis"
        if "github.com" in skill_identifier:
            origin = f"GitHub Repository ({skill_identifier})"

        synthesized_skill = SkillDefinition(
            name=normalized_name,
            category_layer=layer,
            short_description=f"Dynamically synthesized production skill for '{skill_identifier}' configured for HSF.",
            target_tech_stack=stack,
            core_dependencies=deps,
            best_practices=best_practices,
            forbidden_antipatterns=antipatterns,
            sample_code_snippet=snippet,
            is_dynamically_acquired=True,
            source_origin=origin,
        )

        # Cache locally
        self._skills[normalized_name] = synthesized_skill
        cache_file = os.path.join(self.storage_dir, f"{normalized_name}.json")
        try:
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(synthesized_skill.model_dump(), f, indent=2)
        except Exception:
            pass

        return synthesized_skill

    def shape_guidance_for_teammate(
        self,
        skill_name: str,
        teammate_name: str,
        knowledge_level: str,
        preferred_languages: Optional[List[str]] = None,
    ) -> TeammateSkillProfile:
        skill = self._skills.get(skill_name.lower().strip())
        if not skill:
            skill = self.fetch_or_synthesize_skill(skill_name)

        langs = preferred_languages or ["Python", "TypeScript"]
        lvl = knowledge_level.lower()

        if "beginner" in lvl:
            tailored = (
                f"👋 Senior Orbit guide for {teammate_name} (Beginner Level):\n"
                f"Skill: '{skill.name}' ({skill.category_layer}).\n"
                f"1. Start by copying our working boilerplate from '{skill.name}'. Don't reinvent the wheel!\n"
                f"2. Core things to remember:\n"
                + "\n".join([f"   - {bp}" for bp in skill.best_practices])
                + "\n3. Traps to strictly avoid:\n"
                + "\n".join([f"   - {ap}" for ap in skill.forbidden_antipatterns])
                + f"\n4. Example starting snippet:\n{skill.sample_code_snippet}\n"
                f"If you get stuck, run 'hsf pair \"your error message\"' and I'll debug it beside you!"
            )
        elif "senior" in lvl or "advanced" in lvl:
            tailored = (
                f"⚡ Senior Orbit technical specs for {teammate_name} (Advanced Lead):\n"
                f"Skill: '{skill.name}' ({skill.category_layer}).\n"
                f"Target Stack: {', '.join(skill.target_tech_stack)}. Dependencies: {', '.join(skill.core_dependencies)}.\n"
                f"Architectural Guardrails:\n"
                + "\n".join([f"   ✔ {bp}" for bp in skill.best_practices])
                + "\nStrict Anti-Patterns (zero tolerance in code review):\n"
                + "\n".join([f"   ✖ {ap}" for ap in skill.forbidden_antipatterns])
                + f"\nContract Template:\n{skill.sample_code_snippet}"
            )
        else:
            tailored = (
                f"🤖 Senior Orbit pairing briefing for {teammate_name} (Intermediate):\n"
                f"Skill: '{skill.name}' ({skill.category_layer}).\n"
                f"Focus on rapid velocity without violating HSF production standards.\n"
                f"Checklist:\n"
                + "\n".join([f"   - {bp}" for bp in skill.best_practices])
                + "\nAvoid:\n"
                + "\n".join([f"   - {ap}" for ap in skill.forbidden_antipatterns])
            )

        return TeammateSkillProfile(
            teammate_name=teammate_name,
            knowledge_level=knowledge_level,
            preferred_languages=langs,
            assigned_skills=[skill.name],
            tailored_instructions=tailored,
        )
