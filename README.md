# 🚀 Hackathon Strategy Framework (HSF)
### *The Complete Production-Ready Template, Strategy, and Team Workflow for Winning Hackathons*

> **GitHub Repository**: [github.com/Sathvik1533/hackathon-strategy-framework](https://github.com/Sathvik1533/hackathon-strategy-framework)  
> **Core Purpose**: In a 24-hour hackathon, **speed is victory**. Teams that spend 14 hours configuring Docker, wiring database connections, debugging broken imports, and writing repetitive boilerplate end up presenting half-finished toys.  
> **With HSF, your entire production stack is live in 60 seconds.** Your team saves those 14 hours and redirects 100% of your energy into domain business logic and standout, natural-fit AI features.

---

## ⚡ 60-Second Quickstart

```bash
# 1. Clone the repository
git clone https://github.com/Sathvik1533/hackathon-strategy-framework.git
cd hackathon-strategy-framework

# 2. Make scripts executable and boot the full stack
chmod +x init.sh bin/cli.js pitch/generate_pitch.sh pitch/demo.sh infra/deploy_aws.sh
./init.sh
```

### What Is Online Right Away:
* 🌐 **API & Interactive Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
* 💓 **Health & pgvector Check**: [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)
* 🖥️ **Live Frontend Console**: [http://localhost:8000](http://localhost:8000) (serving `frontend/index.html`)
* 🔌 **FastMCP SSE Tool Server**: `http://localhost:8001/sse`
* 🗄️ **PostgreSQL + pgvector**: `localhost:5432` (pre-seeded with 1536-dim vectors)
* ⚡ **Redis Task Broker & Semantic Cache**: `localhost:6379`
* 📊 **Pitch Deck Engine**: `pitch/presentation.html`

---

## 🧭 What to Use on What (The Master Tech Stack Map)

Here is the exact tool to choose for each job in plain, simple English:

| Technology | Role in Stack | In Simple English: What It Does | When to Use It |
| :--- | :--- | :--- | :--- |
| **Python 3.11** | Core Language | The primary runtime for our backend and AI logic. | Always. Required across all services. |
| **FastAPI** | Backend Web Framework | Serves REST endpoints, validates inputs, and streams real-time logs. | Always. Our default API server. |
| **PostgreSQL 16** | Relational Database | Stores users, orders, audit logs, and core business data with ACID safety. | For all structured, relational data. |
| **pgvector** | Vector Extension | Stores and searches vector embeddings inside PostgreSQL using HNSW indexes. | When documents need semantic similarity search. |
| **SQLAlchemy 2.0 + Alembic** | ORM & Migrations | Safely defines database models and applies version-controlled schema updates. | Always. Never write raw unmanaged SQL schemas. |
| **Redis** | In-Memory Cache & Broker | Delivers sub-10ms query caching, task queuing, and live SSE Pub/Sub. | For background job queues and semantic caching. |
| **LangGraph** | Multi-Agent Orchestration | Coordinates multiple specialized agents with loops, memory, and approval gates. | When an AI task requires 2+ steps, tools, or human checks. |
| **LangChain** | LLM Connectors & Prompts | Connects Python cleanly to OpenAI, Anthropic, and Groq models. | For standard prompt templates and chat model calls. |
| **FastMCP** | Model Context Protocol | Wraps CLI tools (FFmpeg, scrapers) into isolated, typed tools over SSE. | Whenever an AI agent needs to call external software safely. |
| **Docker & Docker Compose**| Containerization | Packages the entire application so it runs identically on every computer. | Always. Eliminates "works on my machine" bugs. |
| **AWS ALB** | Load Balancer | Distributes web traffic and handles HTTPS/SSL certificates. | In cloud production in front of our container tasks. |
| **AWS ECS on Fargate** | Serverless Container Host | Runs our Docker containers in AWS without managing virtual servers. | For production deployment of our API and worker tasks. |
| **Amazon ECR** | Docker Registry | Private, secure AWS storage for our built Docker container images. | CI/CD pushes here before ECS deploys. |
| **Amazon S3** | Object Storage | Stores large files like uploaded PDFs, rendered MP4s, and evaluation reports. | Any file bigger than 100KB (never store binaries in Postgres). |
| **AWS DynamoDB** | Fast NoSQL Storage | Ultra-fast key-value storage for session tokens or rate-limit counters. | Optional alternative to Redis if serverless AWS NoSQL is needed. |
| **Marp CLI** | Slide Generator | Converts Markdown notes into high-end HTML and PDF pitch decks in 2 seconds. | For our hackathon pitch deck and stage presentation. |

---

## 🏛️ Layer-by-Layer Architectural Guide

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 1. FRONTEND LAYER (`frontend/`)                                                        │
│ • Responsive, dark-mode console built with clean CSS design tokens (no AI slop).       │
│ • Real-time Server-Sent Events (SSE) listener reading `/api/v1/jobs/{id}/stream`.      │
│ • Animated terminal log box showing live agent thought processes and progress bar.    │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │ HTTP / SSE
┌───────────────────────────────────────────▼────────────────────────────────────────────┐
│ 2. BACKEND API LAYER (`backend/`)                                                      │
│ • FastAPI async app with `@asynccontextmanager lifespan` and connection pool cleanup.  │
│ • Pydantic v2 schemas validating request payloads and enforcing `ResponseEnvelope`.    │
│ • JWT Authentication (`src/app/core/security.py`) for protected endpoints.             │
│ • Global Exception Handlers returning clean JSON error envelopes instead of tracebacks.│
└─────────────────────┬────────────────────────────────────────────────────┬─────────────┘
                      │                                                    │
┌─────────────────────▼──────────────────────────────┐ ┌───────────────────▼─────────────┐
│ 3. DATABASE LAYER (`database/`)                    │ │ 4. AI & AGENT LAYER (`ai_layer/`)│
│ • PostgreSQL 16 with pgvector extension enabled.   │ │ • LangGraph Supervisor Graph.   │
│ • HNSW Cosine Index (`m=16, ef_construction=64`).  │ │ • FastMCP SSE Tool Server.      │
│ • Generated `tsv_content` column for BM25 search.  │ │ • FlashRank 2-Stage Reranker.   │
│ • 3-Second Seed Script (`database/seed_data.py`).  │ │ • Sub-10ms Redis Semantic Cache.│
└────────────────────────────────────────────────────┘ │ • Prompt Injection Guardrails.  │
                                                       │ • RAGAS 25-Case Eval Harness.   │
                                                       └─────────────────────────────────┘
                                            │
┌───────────────────────────────────────────▼────────────────────────────────────────────┐
│ 5. DEPLOYMENT & AWS CLOUD LAYER (`infra/`)                                             │
│ • Multi-stage Dockerfile (<180MB) running as non-root user `appuser`.                  │
│ • `docker-compose.yml` wiring API + pgvector + Redis + FastMCP on an isolated network. │
│ • AWS ECS Fargate task definition (`aws-ecs-task-definition.json`).                    │
│ • 1-Click AWS deployment script (`infra/deploy_aws.sh`).                               │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🛡️ Essential Production Patterns (Simplified for Teammates)

We have built production-grade reliability directly into the framework under [`backend/src/app/core/resilience.py`](backend/src/app/core/resilience.py). Here is what each pattern does:

### 1. Exponential Backoff with Full Jitter
* **What happens without it**: If an external API (like OpenAI) returns a `429 Rate Limit`, a naive script retries immediately. Ten requests retrying at the same time cause a "thundering herd" that crashes the service.
* **How our code fixes it**: We back off exponentially ($0.5\text{s} \rightarrow 1\text{s} \rightarrow 2\text{s} \rightarrow 4\text{s}$) and add **random jitter** so retries are spread out smoothly.
* **Usage**:
  ```python
  from src.app.core.resilience import retry_with_exponential_backoff


  @retry_with_exponential_backoff(max_retries=3, base_delay=0.5)
  async def call_external_llm(prompt: str): ...
  ```

### 2. Circuit Breaker Pattern
* **What happens without it**: If a downstream service (a payment gateway or external scraper) crashes, your backend keeps making calls and hangs while waiting for timeouts. This exhausts your server's memory and freezes the entire app.
* **How our code fixes it**: Our `CircuitBreaker` tracks failures. After 5 consecutive errors, it trips **OPEN** and immediately rejects new requests for 30 seconds without wasting time calling the dead service. After 30 seconds, it enters **HALF-OPEN** to test if the service has recovered.

### 3. Idempotency Keys (Redis Distributed Locks)
* **What happens without it**: A user clicks the "Pay" or "Render Video" button twice because the UI felt slow. Two identical jobs are created, charging the user twice or rendering the video twice.
* **How our code fixes it**: The frontend passes an `Idempotency-Key` header. Redis uses `SETNX` (set if not exists) to lock the key. If the same key arrives again within 120 seconds, the second request receives the cached result instantly without re-executing.

### 4. Dead Letter Queues (DLQ) & Execution Timeouts
* **What it does**: Any background task that fails after 3 retries is placed in a Dead Letter Queue instead of clogging the main queue indefinitely. Celery workers enforce `task_time_limit = 600` so runaway loops are killed automatically.

### 5. Graceful Shutdown & Drain
* **What it does**: When updating code or restarting containers, the app catches `SIGTERM`. It stops accepting new requests, finishes in-flight jobs, flushes database connection pools cleanly, and shuts down with zero data corruption.

---

## ⚖️ Standard Architectural Trade-Offs (Pick the Right Tool)

Every design choice has a trade-off. Use this guide to defend your architecture to hackathon judges:

### Trade-Off 1: Relational SQL (PostgreSQL) vs. NoSQL (DynamoDB)
* **Use PostgreSQL when**: You have relationships between users, tasks, and documents, need ACID transactions, or require vector search (pgvector).
* **Use DynamoDB when**: You only need ultra-high-throughput key-value lookups (e.g., millions of game sessions or simple telemetry pings).
* **Our Default**: **PostgreSQL 16**. It gives us relational integrity AND vector search in one database without managing two separate systems.

### Trade-Off 2: Synchronous Request/Response vs. Asynchronous Task Queue
* **Use Synchronous (< 500ms)**: For logins, simple database reads, and single fast LLM completions.
* **Use Asynchronous Queue + SSE (> 1s)**: For video rendering, multi-step LangGraph research, and bulk document ingestion.
* **Why**: Long-running synchronous HTTP requests tie up web worker threads, leading to gateway timeouts (HTTP 504).

### Trade-Off 3: Dense Vector Search vs. Sparse Keyword (BM25) vs. Hybrid (RRF)
* **Dense Vector Search**: Understands semantic meaning ("automobile" matches "car"), but struggles with exact SKU numbers, names, or order IDs.
* **Sparse Keyword Search**: Finds exact words, but fails when users use synonyms.
* **Our Solution**: **Hybrid Search with Reciprocal Rank Fusion (RRF)**. Combines the best of both directly inside PostgreSQL.

### Trade-Off 4: Fine-Tuning (LoRA) vs. RAG vs. In-Context Prompting
* **Prompting**: Fast and cheap. Try this first.
* **RAG**: Use when the model needs **new, external, or private facts** with verifiable citations.
* **Fine-Tuning (LoRA)**: Use ONLY when you need specialized **output formatting, domain style, or model distillation** to run an 8B model cheaply. Never fine-tune just to add facts.

### Trade-Off 5: AWS ECS on Fargate vs. AWS Lambda
* **Use ECS Fargate**: For our FastAPI server and Celery workers. Supports persistent background threads, SSE streaming, and heavy packages (FFmpeg, PyTorch, LangGraph) without cold starts.
* **Use AWS Lambda**: For tiny, event-driven webhooks that run for only 200ms once an hour.

---

## 📋 Hackathon Problem Statement Readiness Checklist

When you receive a hackathon challenge, walk through this checklist in order:

- [ ] **Step 1: Is this a deterministic problem or an AI problem?**
  - If the answer can be computed with SQL queries, math, or regex, **do not use an LLM**.
- [ ] **Step 2: Does the problem require private documents or dynamic facts?**
  - If YES: Activate the RAG pipeline (`ai_layer/hybrid_retriever.py`).
  - If NO: Use a direct structured prompt (`gpt-4o-mini`).
- [ ] **Step 3: Will the task take more than 1 second to complete?**
  - If YES: Route through the async job queue (`backend/services/job_service.py`) and stream progress to the frontend via SSE.
  - If NO: Return the result synchronously.
- [ ] **Step 4: Can the operation cause financial or data damage?**
  - If YES: Add a Human-in-the-Loop interrupt gate (`ai_layer/langgraph_supervisor.py`).
- [ ] **Step 5: Are external tools or command-line programs needed?**
  - If YES: Wrap them in a FastMCP tool server (`ai_layer/fastmcp_server.py`). Never use raw shell calls.
- [ ] **Step 6: Have we proven accuracy?**
  - Run the evaluation suite (`python ai_layer/eval_harness.py`) and document the RAGAS Faithfulness score on your presentation slides.

---

## 👥 How Teammates Should Use This Repo with Agentic AI IDEs

When your team uses Agentic IDEs (**Antigravity, Cursor, Windsurf**), divide the responsibilities by layer:

### Role 1: Backend & Data Lead
* **Primary Focus**: Define business models in `backend/src/app/models/` and endpoints in `backend/src/app/api/v1/endpoints/`.
* **Skills to Prompt**: Use `fastapi-production-archetype`, `sqlalchemy-alembic-ops`, and `pgvector-hybrid-search`.
* **Prompt to Agent**: *"Create an async endpoint for [feature] following our FastAPI archetype, with Pydantic v2 validation and ResponseEnvelope."*

### Role 2: AI & Agentic Lead
* **Primary Focus**: Build the domain agent in `ai_layer/` using LangGraph or FastMCP.
* **Skills to Prompt**: Use `langgraph-production-patterns`, `fastmcp-tool-server`, and `agent-security-guardrails`.
* **Prompt to Agent**: *"Build a LangGraph supervisor graph for [domain] with state persistence and a human approval gate before database writes."*

### Role 3: Frontend Lead
* **Primary Focus**: Customize `frontend/index.html` with domain-specific cards, inputs, and SSE progress listeners.
* **Skills to Prompt**: Use `hallmark`, `emil-design-eng`, and `awesome-design-systems`.
* **Prompt to Agent**: *"Design a clean, high-density dark mode dashboard for [feature] that connects to our SSE log endpoint on /api/v1/jobs/{id}/stream."*

### Role 4: DevOps & Pitch Lead
* **Primary Focus**: Docker configuration, AWS deployment, evaluation numbers, and Marp pitch slides.
* **Skills to Prompt**: Use `marp-presentation-engine`, `agent-eval-harness`, and `agent-docker-aws-deploy`.
* **Prompt to Agent**: *"Generate a 10-slide Marp pitch deck in pitch/pitch.marp.md covering our problem, architecture, RAGAS metrics, and live demo."*

---

## 🤖 The Automated PR Reviewer Agent

Whenever a teammate creates a Pull Request, our GitHub Action (`.github/workflows/pr-reviewer-agent.yml`) automatically inspects the code:

1. **Scans for Hardcoded Secrets**: Catches leaked OpenAI keys or database passwords.
2. **Checks SQL Safety**: Flags raw string formatting in database queries.
3. **Validates Subprocesses**: Ensures no dangerous `shell=True` calls exist.
4. **Runs Ruff Linting**: Guarantees clean, PEP-8 compliant code.

### Run Local Review Before Pushing:
```bash
python scripts/review_pr.py
```
Output:
```
## 🤖 Automated PR Reviewer Agent Report
### 📋 Automated Verification Checklist
- ✔ No exposed hardcoded API keys detected.
- ✔ Database queries use parameterized binding.
- ✔ Subprocess execution adheres to safe array isolation.
- ✔ Ruff zero-lint errors passed.
### 🎉 Review Status: APPROVED FOR MERGE
```

---

## 📚 Curated Index of Essential Repositories

All official repositories integrated into or referenced by this framework:

| Repository | GitHub Link | Purpose |
| :--- | :--- | :--- |
| **Marp** | [marp-team/marp](https://github.com/marp-team/marp) | Converts Markdown directly into HTML, PDF, and PPTX slide decks. |
| **Context7** | [upstash/context7](https://github.com/upstash/context7) | Real-time version-specific documentation fetcher and MCP server. |
| **Pydantic AI** | [pydantic/pydantic-ai](https://github.com/pydantic/pydantic-ai) | Type-safe Python agent framework with dependency injection. |
| **LangGraph** | [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) | Cyclic multi-agent state graphs with persistence and approval gates. |
| **FastMCP** | [jlowin/fastmcp](https://github.com/jlowin/fastmcp) | High-level Python SDK for Model Context Protocol servers over SSE. |
| **FlashRank** | [PrithivirajDamodaran/FlashRank](https://github.com/PrithivirajDamodaran/FlashRank) | Ultra-fast local neural reranker (<20ms) for 2-stage retrieval. |
| **RAGAS** | [explodinggradients/ragas](https://github.com/explodinggradients/ragas) | Retrieval Augmented Generation evaluation metrics (Faithfulness, Relevance). |
| **Promptfoo** | [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) | CLI-based LLM output testing and prompt regression test runner. |
| **ScrapeGraphAI** | [ScrapeGraphAI/Scrapegraph-ai](https://github.com/ScrapeGraphAI/Scrapegraph-ai) | LLM-powered web scraping pipelines for automated data extraction. |
| **Archify** | [tt-a1i/archify](https://github.com/tt-a1i/archify) | Generates interactive SVG architecture diagrams from code evidence. |
| **Brag** | [latent-spaces/brag](https://github.com/latent-spaces/brag) | Generates technical launch documentation, release notes, and demo scripts. |
| **Graphify** | [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) | AST code knowledge graph extractor for low-token codebase navigation. |
| **Ralph** | [snarktank/ralph](https://github.com/snarktank/ralph) | Slices high-level PRDs into atomic, single-context user stories. |

---

## 🎤 Pitch Deck & Stage Demo Playbook

### 1. Generate Your Slide Deck (Marp)
```bash
# Output interactive HTML slides:
node bin/cli.js pitch
# Output PDF presentation:
marp --pdf pitch/pitch.marp.md -o pitch/pitch_deck.pdf
```
Your slides are already formatted with problem statements, architecture diagrams, evaluation metrics, and live demo steps.

### 2. Live Stage Backup Runner (`pitch/demo.sh`)
If Wi-Fi drops or the frontend projector freezes on stage, open your terminal and run:
```bash
bash pitch/demo.sh
```
In 30 seconds, it triggers the health check, submits an async agent job, and streams live SSE logs with color-coded badges directly in your terminal.

---

## 🏆 Why This Framework Wins Hackathons

1. **Zero Wasted Setup Time**: You skip the first 14 hours of boilerplate setup.
2. **Production Credibility**: Judges see Alembic migrations, HNSW vector indexes, Docker multi-stage builds, and AWS task specs—not fragile toy scripts.
3. **Natural-Fit AI**: The architecture document defends why every AI feature exists with hard metrics, avoiding vanity AI penalties.
4. **Resilient Presentation**: If anything fails on stage, Marp slides and terminal cURL scripts ensure a flawless pitch.

**Built by Sathvik for high-velocity, production-grade hackathon execution.**
