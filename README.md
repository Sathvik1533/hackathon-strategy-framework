# 🚀 Hackathon Strategy Framework (HSF)
### *Production-Grade Architecture, Pre-Ready Templates, and Team Workflow for Winning Hackathons*

> **Repository**: [github.com/Sathvik1533/hackathon-strategy-framework](https://github.com/Sathvik1533/hackathon-strategy-framework)  
> **Core Philosophy**: In a 24-hour hackathon, **speed and focus are everything**. Teams that waste 14 hours wiring Docker, configuring database drivers, fighting CORS, and debugging broken imports inevitably deliver half-finished prototypes.  
> With HSF, your entire multi-service stack (FastAPI, pgvector, Redis, LangGraph, FastMCP, and SSE streaming) is **online in 60 seconds**. Your team spends 100% of the sprint customizing business logic and building standout AI features that naturally solve the problem.

---

## ⚡ 60-Second Quickstart for Teammates

### Option A: 1-Click Bootstrap Script (Recommended)
```bash
git clone https://github.com/Sathvik1533/hackathon-strategy-framework.git
cd hackathon-strategy-framework
chmod +x init.sh bin/cli.js
./init.sh
```

### Option B: Via Runnable CLI (`hsf`)
```bash
# Link the CLI locally
npm link
# Or run directly via npx / node:
node bin/cli.js init
```

### What Spins Up Instantly:
* 🌐 **API & Interactive Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
* 💓 **Health Endpoint**: [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)
* 🖥️ **Frontend Console**: [http://localhost:8000](http://localhost:8000) (serving `frontend/index.html`)
* 🔌 **FastMCP Tool Server**: `http://localhost:8001/sse`
* 🗄️ **PostgreSQL + pgvector**: `localhost:5432` (pre-seeded with 1536-dim vectors)
* ⚡ **Redis Task Broker & Semantic Cache**: `localhost:6379`
* 📊 **Pitch Deck Slide Engine**: `pitch/presentation.html`

---

## 👥 How to Collaborate in a Team (Branch & Agentic IDE Workflow)

When 3–4 developers build together using Agentic IDEs (Antigravity, Cursor, Windsurf), merge conflicts and broken contracts are the #1 killer. We use an **Issue-Driven Branch Strategy**:

```
[Team Lead / Product Owner]
          │
          ├──── Creates GitHub Issue with interface contract (`.github/ISSUE_TEMPLATE`)
          │
          ▼
┌─────────────────────────┬─────────────────────────┬─────────────────────────┐
│ Feature Branch A        │ Feature Branch B        │ Feature Branch C        │
│ `feat/auth-endpoints`   │ `feat/langgraph-agent`  │ `feat/frontend-cards`   │
│ (Developer 1)           │ (Developer 2)           │ (Developer 3)           │
└────────────┬────────────┴────────────┬────────────┴────────────┬────────────┘
             │                         │                         │
             ▼                         ▼                         ▼
      [Opens Pull Request to `main` via Agentic IDE / Git]
                               │
                               ▼
     ┌───────────────────────────────────────────────────┐
     │ 🤖 Automated PR Reviewer Agent                    │
     │ (.github/workflows/pr-reviewer-agent.yml)         │
     │ • Scans diff for SQL injection risks             │
     │ • Checks for hardcoded secrets or API keys        │
     │ • Validates Pydantic response envelopes           │
     │ • Runs Ruff linting & Pytest checks               │
     └─────────────────────────┬─────────────────────────┘
                               │
                 [Status: APPROVED FOR MERGE]
                               │
                               ▼
                       [Merged into `main`]
```

### Teammate Branch Rules:
1. **Never commit directly to `main`**.
2. **Name your branch by layer**:
   - `feat/api-<feature-name>` (Backend changes)
   - `feat/agent-<workflow-name>` (AI / LangGraph changes)
   - `feat/ui-<view-name>` (Frontend changes)
3. **Run local review before pushing**:
   ```bash
   python scripts/review_pr.py
   ```

---

## 🧠 The AI Architectural Decision Framework: When to Use What

> **Judges penalize vanity AI.** Every AI feature must have a specific role or value added to the problem statement. Never use a 70B model or complex graph where standard software engineering solves the problem better.

```
+----------------------------------------------------------------------------------------------------+
| SCENARIO                          | TECHNOLOGY TO USE        | WHEN TO SKIP IT                     |
+----------------------------------------------------------------------------------------------------+
| Exact data lookup, ID queries,    | Pure PostgreSQL SQL      | NEVER use RAG for exact lookups.    |
| numeric ranges, or CRUD filters   | with SQLAlchemy 2.0      | SQL is 1000x faster and exact.      |
+-----------------------------------+--------------------------+-------------------------------------+
| Domain document Q&A, PDF inquiry, | pgvector + BM25          | Skip if data fits in 10 lines of    |
| verifiable factual citations      | Hybrid Search (RRF)      | system prompt context.              |
+-----------------------------------+--------------------------+-------------------------------------+
| Repeated or paraphrased queries   | Redis Semantic Cache     | Skip if queries are always unique   |
| (FAQ lookups, customer support)   | (<12ms, $0.00 cost)      | or require real-time state.         |
+-----------------------------------+--------------------------+-------------------------------------+
| Fast routing, classification,     | Jev / System-One Model   | Skip if task requires creative,     |
| guardrails, safety check (<150ms) | (TypeSafe AI)            | generative paragraphs.              |
+-----------------------------------+--------------------------+-------------------------------------+
| Multi-step tool workflows with    | LangGraph Supervisor     | Skip if task is a single linear     |
| retries and isolated state        | with Postgres checkpts   | prompt (use ChatOpenAI directly).   |
+-----------------------------------+--------------------------+-------------------------------------+
| High-risk irreversible actions     | LangGraph Human-in-the-  | Skip for harmless read-only tasks   |
| (database mutations, payments)    | Loop Interrupt Gate      | that require zero approval.         |
+-----------------------------------+--------------------------+-------------------------------------+
| External tools / CLI execution    | FastMCP Server over SSE  | Never run `subprocess(shell=True)`  |
| (FFmpeg, ElevenLabs, Web APIs)    |                          | directly inside endpoint handlers.  |
+----------------------------------------------------------------------------------------------------+
```

---

## 🏗️ Layer-by-Layer Pre-Ready Templates

### 1. Backend Layer (`backend/`)
* **FastAPI Async Archetype**: Built on Python 3.11 with modern `@asynccontextmanager lifespan`.
* **Standardized JSON Envelope**: Every endpoint returns `{"success": true, "data": {...}, "message": "..."}`, eliminating frontend parsing surprises.
* **Global Error Middleware**: Unhandled exceptions return structured `ErrorEnvelope` rather than raw Python stack traces.
* **Async Database Sessions**: Dependency-injected `get_db` yielding SQLAlchemy 2.0 `AsyncSession`.

### 2. Database & Vector Layer (`database/`)
* **PostgreSQL + pgvector**: Pre-configured with HNSW cosine distance index (`m=16, ef_construction=64`).
* **Hybrid Search with RRF**: PostgreSQL CTE query combining dense vector distance with sparse BM25 `tsvector` ranking:
  $$\text{RRF Score}(d) = \sum_{m \in M} \frac{1}{60 + \text{rank}_m(d)}$$
* **Instant Seed Script**: `python database/seed_data.py` populates 25 domain records with 1536-dim embeddings in 3 seconds.

### 3. AI & Agentic Layer (`ai_layer/`)
* **`langgraph_supervisor.py`**: State graph coordinating researcher and action workers with PostgreSQL checkpoint persistence.
* **`fastmcp_server.py`**: Official Model Context Protocol (MCP) server exposing tools over Server-Sent Events (SSE).
* **`flashrank_reranker.py`**: 2-stage neural reranking taking top 25 broad candidates down to top 5 high-precision chunks in $<20\text{ms}$.
* **`guardrails.py`**: Delimiter-based prompt injection sanitizer and read-only database query validator.
* **`eval_harness.py`**: RAGAS metrics suite (Faithfulness, Answer Relevance) and Promptfoo regression tests.

### 4. Frontend Layer (`frontend/`)
* **Modern Editorial Console**: Built with clean CSS tokens, dark mode, and zero generic AI gradients.
* **Real-Time SSE Log Reader**: Listens to `/api/v1/jobs/{id}/stream` and renders animated progress bars and terminal logs.
* **Pre-connected Dashboard**: Trigger multi-agent jobs and view live metrics directly from your browser.

### 5. Infrastructure & AWS Production Patterns (`infra/`)
* **Multi-Stage Dockerfile**: Slim runner image ($<180\text{MB}$) with non-root security and layer-cached dependencies.
* **docker-compose.yml**: Wires API, pgvector, Redis, and FastMCP on an isolated internal bridge network.
* **AWS ECS / Fargate Deployment**: Production task definition (`aws-ecs-task-definition.json`) and 1-click deployment script (`deploy_aws.sh`).

---

## ⏱️ The 24-Hour Hackathon Winning Playbook

| Timeline | Phase | Deliverables & Milestones |
| :--- | :--- | :--- |
| **Hours 0 – 2** | **Specification & Alignment** | Run `hsf init`. Define business domain in `.env`. Team reviews `ai_layer/decision_matrix.md`. Create GitHub issues for each feature. |
| **Hours 2 – 8** | **Core API & Data Ingestion** | Build domain models in `backend/models/`. Run `database/seed_data.py`. Implement core business endpoints in `backend/api/v1/`. |
| **Hours 8 – 14** | **AI Layer & Agent Orchestration**| Wire domain tools into `ai_layer/fastmcp_server.py`. Assemble LangGraph state graph. Verify Human-in-the-Loop interrupt gate. |
| **Hours 14 – 18**| **Frontend & SSE Log Streaming** | Customize `frontend/index.html` with problem-specific cards. Verify real-time SSE progress streaming from `/stream`. |
| **Hours 18 – 21**| **Evals, Security & Hardening** | Run `python ai_layer/eval_harness.py`. Ensure RAGAS Faithfulness $> 0.85$. Verify prompt injection resistance with `guardrails.py`. |
| **Hours 21 – 24**| **Pitch Deck, Demo & Rehearsal** | Compile Marp pitch deck: `hsf pitch`. Rehearse 3-minute pitch. Test stage backup demo script: `bash pitch/demo.sh`. |

---

## 🎤 Pitch Deck & Stage Demo Playbook

### 1. Instant Pitch Deck Generation (Marp)
Never waste hours in slide software before the deadline:
```bash
# Generate standalone interactive HTML slides:
node bin/cli.js pitch
# Or compile via marp CLI:
marp pitch/pitch.marp.md -o pitch/presentation.html
```
The pitch template (`pitch/pitch.marp.md`) is pre-formatted with:
1. Executive Problem Statement & Cost of Failure.
2. Architecture Diagram (FastAPI + LangGraph + pgvector).
3. Why Our AI Naturally Fits (Anti-vanity AI justification).
4. Hard Evaluation Proof (RAGAS Faithfulness & P95 Latency table).
5. 60-Second Live Demo walkthrough script.

### 2. Live Stage Backup Runner (`pitch/demo.sh`)
If Wi-Fi drops or the frontend projector lags on stage, switch instantly to the automated terminal cURL demo:
```bash
bash pitch/demo.sh
```
It animates health checks, async job submission, and live SSE streaming directly in the terminal in 30 seconds.

---

## 🛠️ Project Structure Overview

```
hackathon-strategy-framework/
├── README.md                      # Complete team handbook and strategy guide
├── pyproject.toml                 # Poetry dependencies & build system
├── package.json                   # CLI wrapper for npx / npm execution
├── init.sh                        # 1-click bootstrap script
├── .env.example                   # Environment variable template
│
├── bin/
│   └── cli.js                     # Runnable CLI (hsf init, pitch, eval, review)
│
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                 # Ruff linting & Pytest CI suite
│   │   └── pr-reviewer-agent.yml  # Automated PR Reviewer Agent
│   └── ISSUE_TEMPLATE/
│       └── hackathon-feature.md   # Standardized feature request for agentic IDEs
│
├── backend/                       # Production FastAPI Async Service
│   ├── src/app/
│   │   ├── main.py                # Application factory, lifespan, CORS, error envelopes
│   │   ├── core/                  # Config, database engine, security JWT
│   │   ├── api/v1/endpoints/      # Health, auth, async jobs, AI agent
│   │   ├── models/                # SQLAlchemy models (TimestampedModel, DocumentChunk)
│   │   └── schemas/               # Pydantic v2 schemas & ResponseEnvelope
│   └── tests/                     # Pytest async test suite
│
├── database/                      # PostgreSQL + pgvector Migration & Seeds
│   ├── alembic/                   # Async Alembic migrations
│   └── seed_data.py               # 3-second database fixture seeder (embeddings included)
│
├── ai_layer/                      # Modular AI & Agentic Components
│   ├── decision_matrix.md         # When to use what (and when NOT to use AI)
│   ├── langgraph_supervisor.py    # Multi-agent supervisor with approval gate
│   ├── fastmcp_server.py          # FastMCP tool server over SSE
│   ├── hybrid_retriever.py        # pgvector + BM25 Reciprocal Rank Fusion
│   ├── flashrank_reranker.py      # 2-stage neural reranking
│   ├── redis_semantic_cache.py    # Sub-10ms vector cache
│   ├── guardrails.py              # Prompt injection defense & SQL validator
│   └── eval_harness.py            # RAGAS & Promptfoo test suite
│
├── frontend/                      # High-Velocity Console
│   ├── index.html                 # Responsive dark-mode dashboard
│   ├── style.css                  # Modern design tokens (anti-AI slop)
│   └── app.js                     # Live SSE event stream listener
│
├── infra/                         # Infrastructure & Cloud Deployment
│   ├── Dockerfile                 # Multi-stage Python 3.11 runner (<180MB)
│   ├── docker-compose.yml         # API + pgvector + Redis + FastMCP stack
│   ├── aws-ecs-task-definition.json # AWS ECS/Fargate task spec
│   └── deploy_aws.sh              # 1-click AWS ECR & ECS deployment
│
├── pitch/                         # Pitch & Stage Presentation
│   ├── pitch.marp.md              # 10-slide Marp pitch deck template
│   ├── generate_pitch.sh          # Export HTML & PDF slides
│   └── demo.sh                    # Live terminal cURL stage backup
│
└── scripts/
    └── review_pr.py               # Local & CI automated PR reviewer agent
```

---

## 🏆 Summary: Why This Wins Hackathons

1. **Zero Wasted Time**: You skip the first 14 hours of boilerplate setup.
2. **Production Credibility**: Judges see Alembic migrations, HNSW indexes, Docker multi-stage builds, and AWS task specs—not fragile toy scripts.
3. **Natural-Fit AI**: The architecture document defends why every AI feature exists with hard metrics, avoiding vanity AI penalties.
4. **Resilient Presentation**: If anything fails on stage, Marp slides and terminal cURL scripts ensure a flawless pitch.

**Built by Sathvik for high-velocity, production-grade hackathon execution.**
