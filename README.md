# 🚀 Hackathon Strategy Framework (HSF)
### *Production-Grade Architecture, Pre-Ready Templates, and Team Workflow for Winning Hackathons*

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

### What Is Online Instantly:
* 🌐 **API & Interactive Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
* 💓 **Health & pgvector Check**: [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)
* 🖥️ **Live Frontend Console**: [http://localhost:8000](http://localhost:8000) (serving `frontend/index.html`)
* 🔌 **FastMCP SSE Tool Server**: `http://localhost:8001/sse`
* 🗄️ **PostgreSQL + pgvector**: `localhost:5432` (pre-seeded with 1536-dim vectors)
* ⚡ **Redis Task Broker & Semantic Cache**: `localhost:6379`
* 📊 **Pitch Deck Engine**: `pitch/presentation.html`

---

## 🏗️ Master Full-Stack Architecture Diagram

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                   FRONTEND LAYER                                       │
│  Native High-Density Console (HTML5/CSS3/Vanilla JS) • Real-Time SSE Log Terminal      │
│  Metric Summary Cards • Status Badges (ENQUEUEING ➔ STREAMING SSE ➔ COMPLETED)          │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │ HTTP / Server-Sent Events (SSE)
┌───────────────────────────────────────────▼────────────────────────────────────────────┐
│                             BACKEND API LAYER (FastAPI)                                │
│  Lifespan Context Manager • Dependency Injection (get_db) • Pydantic v2 Envelopes     │
│  JWT Authentication • Global Exception Interceptor • Background Task Dispatcher         │
└──────────────────────┬─────────────────────────────────────────┬───────────────────────┘
                       │                                         │
┌──────────────────────▼─────────────────┐     ┌─────────────────▼───────────────────────┐
│     DATABASE & STORAGE LAYER           │     │          AI & AGENTIC LAYER             │
│ • PostgreSQL 16 (Relational ACID)      │     │ • LangGraph Cyclic Supervisor Graph     │
│ • pgvector 1536-dim HNSW Cosine Index  │     │ • Human-in-the-Loop Interrupt Gate      │
│ • TSVECTOR GIN Full-Text Index         │     │ • FastMCP Isolated SSE Tool Server      │
│ • Supabase Row-Level Security (RLS)    │     │ • Hybrid Dense + Sparse Retriever (RRF) │
│ • Alembic Zero-Downtime Migrations     │     │ • FlashRank Cross-Encoder Reranker      │
│ • Amazon S3 Object Blob Storage        │     │ • Jev System-1 Fast Decision Router     │
└──────────────────────┬─────────────────┘     │ • Prompt Injection Defense Guardrails   │
                       │                       │ • RAGAS Evaluation Test Harness (QA)    │
                       │                       └─────────────────┬───────────────────────┘
┌──────────────────────▼─────────────────────────────────────────▼───────────────────────┐
│                     PRODUCTION RESILIENCE & CACHING LAYER                              │
│ • Exponential Backoff with Full Jitter • Circuit Breaker (CLOSED / OPEN / HALF-OPEN)    │
│ • Redis Distributed Idempotency Guard (SETNX) • Sub-10ms Semantic Query Cache           │
│ • Sliding-Window Rate Limiter • Session Token Budget Counters                          │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │ Containerized Deployment
┌───────────────────────────────────────────▼────────────────────────────────────────────┐
│                    DEPLOYMENT & AWS INFRASTRUCTURE LAYER                               │
│ • Multi-Stage Docker Build (<180MB) • Docker Compose Local Orchestration               │
│ • AWS ALB (SSL Termination) • AWS ECS on Fargate (Serverless) • Amazon ECR              │
│ • Amazon S3 (Files >100KB) • Amazon DynamoDB (Key-Value) • CloudWatch Telemetry        │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🧭 Core Components, Structure, and Sub-Layers Across All Stacks
*(Detailed Breakdown with the 6D Framework: What, Why, How, When, Where, and Why NOT X)*

---

### 1. FRONTEND LAYER

#### 🧩 Core Components (The 6 Building Blocks):
1. **Layout Shell & Viewport Container (`frontend/index.html`)**: Responsive header, grid cards, split-pane layout with high visual density.
2. **Design System & CSS Token Hierarchy (`frontend/style.css`)**: Dark-mode palette using HSL variables (`--bg-primary: #0a0d14`, `--accent-blue: #3b82f6`, `--accent-emerald: #10b981`), zero layout shifts.
3. **Reactive SSE Event Consumer (`frontend/app.js`)**: Native browser `EventSource` listening to `/api/v1/jobs/{id}/stream`.
4. **Animated Terminal & Log Console**: Auto-scrolling terminal window displaying real-time agent execution logs with timestamps.
5. **State & Progress Indicators**: Dynamic color-coded status badges (`ENQUEUEING`, `STREAMING SSE`, `COMPLETED`, `ERROR`) and an animated progress bar.
6. **Metric KPI Display Cards**: Real-time performance indicators showing RAGAS Faithfulness, Latency P95, and Cache Hit Rate.

#### 🗂️ Core Structure:
```
frontend/
├── index.html       # Clean semantic DOM structure, no build step required
├── style.css        # Modular design tokens, typography, terminal styling, keyframes
└── app.js           # Form submission, async fetch client, SSE listener, log stream
```

#### 🥞 Core Sub-Layers:
* **Presentation Sub-Layer**: High-contrast, dark-mode UI elements built with standard HTML5 and CSS Grid/Flexbox.
* **Client State & Ingress Sub-Layer**: Manages the local UI state machine (`IDLE` ➔ `ENQUEUEING` ➔ `STREAMING` ➔ `COMPLETED` / `FAILED`).
* **HTTP Dispatcher Sub-Layer**: Lightweight `fetch` client sending JSON commands to the backend with error handling and retry guards.

#### 🎯 The 6D Architectural Breakdown:
* **WHAT should be there**: A zero-dependency, ultra-fast frontend featuring an active execution terminal that proves live backend reasoning to judges.
* **WHY it should be there**: Hackathon judges evaluate prototypes visually within 3 minutes. A live terminal streaming real-time Server-Sent Events proves your agent is performing genuine multi-step execution rather than returning pre-baked static answers.
* **HOW it should be there**: Built using native HTML5, modern CSS custom properties, and native JavaScript `EventSource`. Served directly as static assets from FastAPI.
* **WHEN it should be there**: Available immediately from Hour 0 as a working demo, then tailored with problem-specific cards during Hours 14–18.
* **WHERE it should be there**: In the `frontend/` directory, mounted at the root path `http://localhost:8000/`.
* **Why NOT X**:
  * *Why NOT a heavy Next.js / React build?* In a fast-paced sprint, complex React setups frequently encounter Node version mismatches, hydration mismatches, and Webpack build errors that waste hours. This native stack gives 100% of the visual fidelity with zero build fragility.

---

### 2. BACKEND API LAYER (FastAPI)

#### 🧩 Core Components (The 6 Core FastAPI Parts):
1. **Lifespan Context Manager (`@asynccontextmanager lifespan`)**: Initializes database connection pools, verifies Redis availability on startup, and gracefully terminates connections on shutdown.
2. **Dependency Injection Provider (`Depends(get_db)`)**: Yields an isolated SQLAlchemy `AsyncSession` per HTTP request, auto-rolling back failed transactions and releasing connections back to the pool.
3. **Pydantic v2 Type Validation**: Enforces strict request payloads, field constraints, and response schemas via Rust-powered validation.
4. **Standardized Response Envelopes**: Uniform `ResponseEnvelope[T]` (`success`, `data`, `error`, `timestamp`) preventing ambiguous response structures across endpoints.
5. **Middleware Pipeline**: Configured CORS origins, unique `X-Request-ID` generation, process timing headers (`X-Process-Time`), and a global unhandled exception handler.
6. **Background Task & SSE Dispatcher (`JobService`)**: Decouples CPU-heavy or LLM-intensive workflows from HTTP request-response cycles, publishing status updates to Redis Pub/Sub.

#### 🗂️ Core Structure:
```
backend/src/app/
├── core/
│   ├── config.py         # Pydantic BaseSettings loading validated .env variables
│   ├── database.py       # Async SQLAlchemy engine and sessionmaker pool
│   ├── security.py       # JWT token encoding, decoding, and password hashing
│   ├── resilience.py     # Exponential backoff, Circuit Breaker, IdempotencyGuard
│   └── redis.py          # Unified Redis connection pool and key topology manager
├── api/v1/
│   ├── api.py            # Master API router aggregating sub-routers
│   └── endpoints/
│       ├── health.py     # Liveness/readiness probes with DB and pgvector checks
│       ├── documents.py  # Document upload, chunking, and vector search routes
│       └── jobs.py       # Async task triggering and real-time SSE stream routes
├── models/               # SQLAlchemy 2.0 ORM database entity definitions
├── schemas/              # Pydantic v2 request, response, and envelope schemas
└── services/             # Domain business logic and LangGraph agent coordinators
```

#### 🥞 Core Sub-Layers:
* **Transport & Routing Sub-Layer**: Handles URL routing, header parsing, path validation, and HTTP status code mapping.
* **Domain Service Sub-Layer**: Implements business rules, coordinates database transactions, and invokes AI workflows.
* **Data Access & Persistence Sub-Layer**: Interacts with PostgreSQL using async SQLAlchemy queries and typed statements.
* **Resilience & Fault-Tolerance Sub-Layer**: Wraps downstream calls with circuit breakers, retry decorators, and mutex locks.

#### 🎯 The 6D Architectural Breakdown:
* **WHAT should be there**: A high-performance, asynchronous REST API architecture built on FastAPI, SQLAlchemy 2.0, and Pydantic v2.
* **WHY it should be there**: AI agent calls and complex pipelines can take anywhere from 2 to 30 seconds. Synchronous frameworks block worker threads during these delays, causing request timeouts. FastAPI natively supports non-blocking asynchronous execution.
* **HOW it should be there**: Organized into clean separation of concerns: `core/`, `api/v1/`, `models/`, `schemas/`, and `services/`.
* **WHEN it should be there**: Used continuously as the central gateway connecting the client, database, cache, and AI agent graph.
* **WHERE it should be there**: In `backend/src/app/`, run via `uvicorn src.app.main:app`.
* **Why NOT X**:
  * *Why NOT Flask?* Flask is synchronous by default. Long-running AI operations quickly exhaust thread pools and trigger gateway timeouts.
  * *Why NOT Django?* Django's extensive ORM and monolithic setup introduce unnecessary overhead when building agile multi-agent state systems.

---

### 3. DATABASE & STORAGE LAYER (PostgreSQL + pgvector + Supabase RLS + Redis + S3)

#### 🧩 Core Components (The 7 Data Building Blocks):
1. **Relational ACID Engine (PostgreSQL 16)**: Provides strict data integrity guarantees:
   * **Atomicity**: All document chunk insertions and embedding updates either commit together or roll back completely.
   * **Consistency**: Guaranteed through foreign keys (`REFERENCES auth.users(id)`), dimension checks, and NOT NULL rules.
   * **Isolation**: Defaults to "Read Committed" isolation, preventing dirty uncommitted reads between concurrent workers.
   * **Durability**: Write-Ahead Logging (WAL) ensures committed transactions survive unexpected container crashes.
2. **Vector Similarity Engine (`pgvector`)**: Native `embedding Vector(1536)` column indexed with **HNSW Cosine** (`m = 16, ef_construction = 64`) for sub-10ms nearest-neighbor retrieval.
3. **Full-Text Lexical Search Engine**: Generated `tsv_content TSVECTOR` column backed by a GIN inverted index for BM25 keyword matching.
4. **Row-Level Security (RLS) Engine (`database/supabase_rls.sql`)**: Supabase-compatible security policies that enforce multi-tenant isolation based on `auth.uid()`, preventing unauthorized tenant data leaks.
5. **Read-Only Agent Role**: Dedicated PostgreSQL role restricted to `SELECT` permissions, ensuring prompt injections cannot execute destructive `DROP` or `DELETE` commands.
6. **In-Memory Cache & Message Broker (Redis 7)**: Low-latency store managing semantic query caching, SSE channels, distributed idempotency locks, and token rate limits.
7. **Durable Object Storage (Amazon S3 / Supabase Storage)**: Secure object storage for large binary files (>100KB), such as source PDFs, rendered media, and evaluation datasets.

#### 🗂️ Core Structure:
```
database/
├── alembic.ini           # Alembic configuration for async migrations
├── alembic/
│   ├── env.py            # Async migration runner connected to SQLAlchemy metadata
│   └── versions/         # Version-controlled schema migration scripts
├── seed_data.py          # 3-second database seeder with pre-computed vector chunks
└── supabase_rls.sql      # Production RLS policies and role isolation rules

backend/src/app/core/
└── redis.py              # Redis connection pool and key topology manager
```

#### 🥞 Core Sub-Layers:
* **Relational Transaction Sub-Layer**: Manages relational tables, foreign key constraints, and transactional consistency.
* **Vector & Lexical Retrieval Sub-Layer**: Executes combined cosine distance queries and BM25 text searches via PostgreSQL.
* **Security & Access Control Sub-Layer**: Enforces RLS policies at the database layer, verifying identity regardless of application logic bugs.
* **In-Memory Volatile Sub-Layer**: Manages ephemeral keys, Pub/Sub message routing, and TTL-governed semantic caches in Redis.
* **Object Storage Sub-Layer**: Stores large binary assets in Amazon S3, referenced by URI pointers in PostgreSQL records.

#### 🎯 The 6D Architectural Breakdown:
* **WHAT should be there**: A unified storage foundation combining PostgreSQL 16 (relational data + pgvector embeddings + Supabase RLS) with Redis (caching + Pub/Sub) and S3 (object blobs).
* **WHY it should be there**: Using a standalone vector database alongside an application database introduces data sync discrepancies, requires multiple clients, and doubles cloud costs. PostgreSQL with pgvector provides ACID safety and vector similarity in one unified, battle-tested system.
* **HOW it should be there**: Defined declaratively via SQLAlchemy models, managed via Alembic migrations, secured by SQL RLS policies, and seeded instantly using `database/seed_data.py`.
* **WHEN it should be there**: Online prior to application startup, orchestrated via Docker Compose or managed cloud services.
* **WHERE it should be there**: Local container on port `5432`, or managed instances on Supabase or Amazon RDS.
* **Why NOT X**:
  * *Why NOT Pinecone alone?* Pinecone lacks relational tables, transactions, and foreign keys. Joining vector matches with user accounts or billing data requires inefficient multi-database queries.
  * *Why NOT MongoDB?* MongoDB does not offer the same mature HNSW vector graph indexing performance or strict relational ACID constraints needed for multi-tenant applications.

---

### 4. AI & AGENTIC LAYER (LangGraph + FastMCP + RAG + Guardrails + Evals)

#### 🧩 Core Components (The 8 AI Building Blocks):
1. **LangGraph Supervisor Graph (`ai_layer/langgraph_supervisor.py`)**: Cyclic state machine coordinating specialized worker nodes with PostgreSQL checkpoint persistence (`AsyncPostgresSaver`).
2. **Human-in-the-Loop Interrupt Gate**: Configured via `interrupt_before=["human_gate"]`, halting execution before sensitive actions (file writes, financial transactions) until explicit approval is granted.
3. **FastMCP SSE Tool Server (`ai_layer/fastmcp_server.py`)**: Model Context Protocol server exposing isolated tools (shell execution, scrapers, data fetchers) over HTTP Server-Sent Events.
4. **Hybrid Search Retriever (`ai_layer/hybrid_retriever.py`)**: Combines dense cosine similarity with sparse BM25 keyword matching using Reciprocal Rank Fusion (RRF, $k=60$).
5. **FlashRank Neural Cross-Encoder Reranker (`ai_layer/flashrank_reranker.py`)**: Local cross-encoder reranking the top 25 broad candidates down to the top 5 high-precision chunks in $<20\text{ms}$.
6. **Jev System-1 Fast Decision Router (`ai_layer/jev_decision_router`)**: Low-latency typed classifier that routes user queries without waiting for slow generative LLM tokens.
7. **Prompt Injection Defense Guardrails (`ai_layer/guardrails.py`)**: Sanitizes incoming user inputs, strips dangerous injection phrases, and blocks unauthorized SQL verbs.
8. **Automated Evaluation Harness (`ai_layer/eval_harness.py`)**: Automated 25-case golden dataset test runner measuring RAGAS Faithfulness and Answer Relevance metrics.

#### 🗂️ Core Structure:
```
ai_layer/
├── langgraph_supervisor.py   # State graph, agent nodes, and human approval gates
├── fastmcp_server.py         # FastMCP tool server over Server-Sent Events (SSE)
├── hybrid_retriever.py       # Dense pgvector + Sparse BM25 Reciprocal Rank Fusion
├── flashrank_reranker.py     # Sub-20ms neural cross-encoder candidate reranker
├── guardrails.py             # Prompt injection sanitizer and SQL verb validator
├── eval_harness.py           # 25-case golden dataset runner measuring RAGAS scores
└── redis_semantic_cache.py   # Embedding-based semantic response cache
```

#### 🥞 Core Sub-Layers:
* **Ingestion & Embedding Sub-Layer**: Splits documents into chunks, generates 1536-dim embeddings, and writes to PostgreSQL.
* **Routing & Planning Sub-Layer**: Performs fast intent classification using the Jev decision router and orchestrates LangGraph execution paths.
* **Retrieval & Reranking Sub-Layer**: Executes hybrid dense/sparse search, combines scores with RRF, and filters candidates via FlashRank.
* **Execution & Tool Sub-Layer**: Invokes external tools via FastMCP over SSE within isolated sandboxes.
* **Validation & Safety Sub-Layer**: Evaluates outputs against security guardrails and validates semantic faithfulness.

#### 🎯 The 6D Architectural Breakdown:
* **WHAT should be there**: A modular multi-agent system featuring cyclic state graphs, human approval gates, hybrid retrieval, neural reranking, and automated evaluation.
* **WHY it should be there**: Ungrounded monolithic prompts hallucinate, fail on edge cases, and cannot recover from tool failures. Structured agent graphs with verification gates deliver reliable, production-grade behavior.
* **HOW it should be there**: Implemented as independent Python modules with clear input/output schemas that integrate into FastAPI routes or worker tasks.
* **WHEN it should be there**: Activated whenever a task requires complex reasoning, document grounding, or external tool execution.
* **WHERE it should be there**: Located in `ai_layer/` and invoked by backend domain services.
* **Why NOT X**:
  * *Why NOT a single giant prompt?* Monolithic prompts fail under unexpected edge cases, consume excessive tokens on every turn, and lack the ability to selectively retry individual failed steps.

---

### 5. PRODUCTION RESILIENCE & CACHING LAYER

#### 🧩 Core Components (The 5 Resilience Building Blocks):
1. **Exponential Backoff with Full Jitter (`backend/src/app/core/resilience.py`)**:
   $$\text{delay} = \min(\text{max\_delay}, \text{uniform}(0, \text{base\_delay} \times 2^{\text{attempt}}))$$
   Decorates external API calls to prevent synchronized thundering herd spikes during upstream rate limits.
2. **Three-State Circuit Breaker (`CircuitBreaker`)**:
   * **CLOSED**: Normal operation; passes calls through.
   * **OPEN**: Trips after 5 consecutive failures, failing fast immediately for 30 seconds to conserve system resources.
   * **HALF-OPEN**: Allows a single trial request to verify if the downstream dependency has recovered.
3. **Distributed Idempotency Guard (`IdempotencyGuard`)**: Uses Redis `SETNX` mutex locks to guarantee that sensitive operations (billing, video generation) execute exactly once.
4. **Sub-10ms Semantic Cache (`SemanticCache`)**: Caches previous LLM responses keyed by query hashes, reducing token costs and returning responses in $<10\text{ms}$.
5. **Unified Redis Key Topology (`backend/src/app/core/redis.py`)**:
   * `cache:semantic:<hash>`: Stored LLM response payloads.
   * `channel:jobs:<uuid>`: Real-time SSE Pub/Sub message channels.
   * `state:jobs:<uuid>`: Latest job progress snapshots for reconnecting clients.
   * `lock:idempotency:<key>`: Distributed mutex locks (TTL 120s).
   * `ratelimit:<id>:<window>`: Sliding-window rate limit counters.
   * `budget:tokens:<session_id>`: Cumulative session token spend trackers.

#### 🗂️ Core Structure:
```
backend/src/app/core/
├── resilience.py   # Backoff decorators, CircuitBreaker state machine, IdempotencyGuard
└── redis.py        # Redis connection pool, async client provider, key schema topology
```

#### 🥞 Core Sub-Layers:
* **Ingress Rate Protection Sub-Layer**: Inspects incoming requests against sliding-window limits and session token budgets.
* **Egress Fault Protection Sub-Layer**: Wraps external API requests in exponential backoff and circuit breaker protection.
* **Concurrency & Deduplication Sub-Layer**: Enforces distributed locks and caches idempotent results across worker nodes.

#### 🎯 The 6D Architectural Breakdown:
* **WHAT should be there**: Comprehensive fault-tolerance patterns including jittered backoff, circuit breaking, idempotency locks, and semantic caching.
* **WHY it should be there**: Third-party APIs inevitably experience rate limits, transient latency, and occasional outages during live demonstrations. Without automated resilience, a single 429 response can crash an entire presentation.
* **HOW it should be there**: Applied as clean asynchronous decorators (`@retry_with_exponential_backoff`) and reusable helper classes.
* **WHEN it should be there**: Active across all network boundaries, external LLM calls, and database operations.
* **WHERE it should be there**: In `backend/src/app/core/resilience.py` and `backend/src/app/core/redis.py`.
* **Why NOT X**:
  * *Why NOT a naive `while True: sleep(1)` retry loop?* Naive retry loops bombard struggling downstream services with synchronized requests, exacerbating outages and causing permanent rate-limit bans.

---

### 6. DEPLOYMENT & AWS CLOUD LAYER

#### 🧩 Core Components (The 7 Infrastructure Building Blocks):
1. **Multi-Stage Dockerfile (`infra/Dockerfile`)**: Compiles dependencies in a build stage and copies artifacts into a minimal runtime image ($<180\text{MB}$) executed by a non-root `appuser`.
2. **Local Multi-Container Orchestrator (`infra/docker-compose.yml`)**: Coordinates API, PostgreSQL (pgvector), Redis, and FastMCP on an isolated internal network with health probes.
3. **AWS Application Load Balancer (ALB)**: Manages public HTTPS traffic, terminates TLS certificates, and routes requests to healthy backend containers via `/api/v1/health`.
4. **AWS ECS on Fargate**: Serverless container execution eliminating the need to patch, scale, or maintain virtual server operating systems.
5. **Amazon Elastic Container Registry (ECR)**: Secure, private container registry storing immutable, versioned Docker image tags.
6. **Amazon S3 Object Storage**: Scalable object storage for files $>100\text{KB}$ with pre-signed URL generation.
7. **Amazon DynamoDB**: Low-latency NoSQL storage for fast session state management and transient cache requirements.

#### 🗂️ Core Structure:
```
infra/
├── Dockerfile                      # Multi-stage build with non-root security user
├── docker-compose.yml              # Local multi-service environment (API, DB, Redis, MCP)
├── aws-architecture.md             # Complete AWS cloud infrastructure reference
├── aws-ecs-task-definition.json    # Production ECS Fargate task definition
└── deploy_aws.sh                   # Automated build, ECR push, and ECS update script
```

#### 🥞 Core Sub-Layers:
* **Ingress & Networking Sub-Layer**: VPC, public and private subnets, security groups, route tables, and Application Load Balancer.
* **Compute & Container Sub-Layer**: ECS Cluster running Fargate task definitions with automated rolling deployments.
* **Storage & Persistence Sub-Layer**: Amazon RDS PostgreSQL (or Supabase), Amazon S3 buckets, and Amazon DynamoDB tables.
* **Telemetry & Monitoring Sub-Layer**: Amazon CloudWatch container logs, task metrics, and automated health checks.

#### 🎯 The 6D Architectural Breakdown:
* **WHAT should be there**: A complete infrastructure pipeline encompassing multi-stage Docker packaging, local Compose orchestration, and serverless AWS ECS Fargate hosting.
* **WHY it should be there**: Eliminates "works on my machine" issues. Judges and enterprise evaluators look for live, deployed URLs and production-ready cloud architectures.
* **HOW it should be there**: Configured via Infrastructure-as-Code files (`aws-ecs-task-definition.json`), container configurations, and automated deploy scripts (`infra/deploy_aws.sh`).
* **WHEN it should be there**: Tested locally from Day 1 via Docker Compose and deployed to AWS before final presentations.
* **WHERE it should be there**: Encapsulated within the `infra/` directory.
* **Why NOT X**:
  * *Why NOT raw EC2 virtual servers?* EC2 instances require manual OS patching, security group updates, and manual scaling, which wastes valuable time during a hackathon.
  * *Why NOT free-tier sleeping serverless hosts?* Free tiers spin down after periods of inactivity, drop long-lived SSE streaming connections, and lack support for custom binary utilities like FFmpeg.

---

### 7. PITCH, PRESENTATION & DEMO LAYER

#### 🧩 Core Components (The 4 Pitch Building Blocks):
1. **Marp Presentation Engine (`pitch/pitch.marp.md`)**: Slide deck authored in Markdown featuring modern dark-mode styling, architecture diagrams, and metric tables.
2. **Instant Slide Compiler (`node bin/cli.js pitch`)**: Generates interactive HTML and standalone PDF slide decks in under 2 seconds.
3. **Live Stage Fail-Safe Runner (`pitch/demo.sh`)**: Interactive shell script that executes API endpoints and streams colored logs directly in the terminal if Wi-Fi fails or browser tabs freeze on stage.
4. **Evaluation Benchmark Reporter**: Summarizes RAGAS evaluation metrics, P95 latency numbers, and token cost savings directly on the presentation slides.

#### 🗂️ Core Structure:
```
pitch/
├── pitch.marp.md         # Slide source code containing narrative, architecture, and metrics
├── generate_pitch.sh     # Shell script to build HTML and PDF presentations
├── demo.sh               # Live terminal fallback demo runner using cURL
└── presentation.html     # Pre-compiled, fully self-contained offline slide deck
```

#### 🥞 Core Sub-Layers:
* **Narrative & Storytelling Sub-Layer**: Follows the 6-part winning hackathon structure: Hook ➔ Problem ➔ Architecture ➔ Live Demo ➔ Quantitative Metrics ➔ Business Impact.
* **Stage Reliability Sub-Layer**: Dual-mode demonstration strategy: Primary interactive browser console backed by a terminal-based cURL script as an offline fallback.

#### 🎯 The 6D Architectural Breakdown:
* **WHAT should be there**: A code-first presentation system (Marp) paired with a scripted terminal demo fallback.
* **WHY it should be there**: Hackathon Wi-Fi networks frequently become congested during live demonstrations. Having an automated, terminal-based fallback ensures your presentation never stalls on stage.
* **HOW it should be there**: Authored in Markdown, compiled into HTML/PDF, and accompanied by executable demonstration scripts.
* **WHEN it should be there**: Drafted early during Hours 10–12 and finalized with benchmark numbers during Hours 20–22.
* **WHERE it should be there**: In the `pitch/` directory.
* **Why NOT X**:
  * *Why NOT PowerPoint or Canva?* Traditional presentation tools require manual styling, separate design assets, and cannot be version-controlled in Git alongside your codebase.

---

## ⚖️ The Master Architectural Trade-Offs Matrix

| Decision Area | Option A | Option B | Selected Strategy & Trade-Off Rationale |
| :--- | :--- | :--- | :--- |
| **Database** | Relational SQL (Postgres 16) | NoSQL (DynamoDB) | **PostgreSQL 16**. Combines relational ACID safety with pgvector HNSW search in one database. Use DynamoDB only if the prompt requires simple, massive key-value lookups. |
| **API Execution** | Synchronous REST (<500ms) | Async Task Queue + SSE (>1s) | **Split by Latency Budget**. Logins and simple reads are synchronous. Video rendering, LangGraph research, and bulk ingestion use the async queue with live SSE progress streaming. |
| **Search Retrieval** | Pure Dense Vector Search | Pure Sparse Keyword (BM25) | **Hybrid Search with Reciprocal Rank Fusion (RRF)**. Dense search understands meaning; BM25 matches exact SKU/order IDs. Combining both provides zero-compromise accuracy. |
| **Model Customization**| LoRA Fine-Tuning | Retrieval-Augmented Generation | **RAG First**. RAG injects fresh facts with citations without retraining. Use LoRA only when you need strict proprietary output formatting or model distillation. |
| **Cloud Hosting** | AWS ECS on Fargate | AWS Lambda Functions | **ECS Fargate**. Long-running agent loops, SSE streams, and binary tools (FFmpeg) exceed Lambda's execution limits and suffer from cold starts. |
| **Slide Deck** | PowerPoint / Keynote | Marp Markdown Engine | **Marp**. Version-controlled alongside the code, updates in 2 seconds via CLI, and produces offline-ready HTML and PDF decks. |

---

## 🛠️ How Teammates Should Use This Repo in Agentic IDEs
*(Antigravity, Cursor, Windsurf)*

When collaborating in an AI-powered IDE, follow this standardized workflow to maximize speed and maintain codebase integrity:

### 1. Antigravity Slash Commands:
* `/goal`: Launch a long-running, autonomous sprint task (e.g., overnight feature completion) that continues until all validation tests pass.
* `/plan`: Create an explicit step-by-step breakdown of user stories, database models, and endpoints before writing code.
* `/boost`: Engage comprehensive architectural analysis, edge-case validation, and security auditing.
* `/browser`: Test deployed web interfaces, verify API routes, and inspect UI components.

### 2. Antigravity Artifacts (How to Read & Review):
* **What They Are**: Artifacts are persistent markdown documents generated by the agent (`implementation_plan.md`, `walkthrough.md`, architecture diagrams).
* **Why Use Them**: They serve as a contract between teammates. Before any agent writes complex code, review the artifact to ensure alignment on database schema and API contracts.
* **Review Protocol**:
  1. Inspect the Mermaid flowcharts in the plan artifact to verify data boundaries.
  2. Confirm database schemas match `database/supabase_rls.sql` conventions.
  3. Click the UI confirmation button to allow the agent to execute code generation.

### 3. IDE Context Tags:
* `@codebase`: Directs the AI model to index local project files, ensuring generated code adheres to existing conventions.
* `@docs`: Instructs Context7 to fetch up-to-date documentation for libraries without relying on stale training data.
* `@web`: Performs live web searches to look up API changes or troubleshooting guides.

---

### 4. Teammate Role Division & Skill Mapping:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ TEAMMATE 1: BACKEND & DATA LEAD                                                        │
│ • Focus: Models in `backend/models/`, endpoints in `backend/api/v1/`, migrations.     │
│ • Skills to Use:                                                                       │
│   - `fastapi-production-archetype`: Scaffolds endpoints with Pydantic v2 & envelopes.  │
│   - `sqlalchemy-alembic-ops`: Generates zero-downtime Alembic migrations.              │
│   - `pgvector-hybrid-search`: Sets up HNSW indexes and RRF hybrid retrieval queries.   │
│ • Prompt to Agent: "Create an async endpoint for [feature] following our FastAPI       │
│   archetype, with Pydantic v2 validation, database dependency, and ResponseEnvelope."  │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ TEAMMATE 2: AI & AGENTIC LEAD                                                          │
│ • Focus: State graphs in `ai_layer/`, MCP tools, prompt security, and evals.           │
│ • Skills to Use:                                                                       │
│   - `langgraph-production-patterns`: Builds supervisor graphs with approval gates.     │
│   - `fastmcp-tool-server`: Wraps external software into isolated SSE tools.           │
│   - `agent-security-guardrails`: Adds prompt injection sanitizers & read-only DB locks.│
│   - `agent-eval-harness`: Generates 25 golden test cases and measures RAGAS scores.    │
│ • Prompt to Agent: "Build a LangGraph supervisor graph for [domain] with state         │
│   persistence and a human approval gate before database writes."                       │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ TEAMMATE 3: FRONTEND LEAD                                                              │
│ • Focus: Dashboard cards, real-time SSE progress streaming, styling, responsiveness.   │
│ • Skills to Use:                                                                       │
│   - `hallmark`: Anti-AI-slop design constraints and clean typography.                  │
│   - `emil-design-eng`: Polished 150-220ms spring physics and micro-interactions.       │
│   - `awesome-design-systems`: Tokenized design systems and responsive components.      │
│ • Prompt to Agent: "Design a clean dark-mode dashboard for [feature] that connects     │
│   to our SSE log stream on /api/v1/jobs/{id}/stream and renders live progress."        │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ TEAMMATE 4: DEVOPS & PITCH LEAD                                                        │
│ • Focus: Docker Compose, AWS ECS Fargate, Marp slide decks, live stage demo rehearsal. │
│ • Skills to Use:                                                                       │
│   - `marp-presentation-engine`: Compiles Markdown notes into high-end HTML/PDF slides. │
│   - `agent-docker-aws-deploy`: Verifies multi-stage Docker builds and AWS ECS specs.   │
│   - `hackathon-speedrun-kit`: Runs seed data scripts and interactive terminal demos.   │
│ • Prompt to Agent: "Compile our pitch deck in pitch/pitch.marp.md into HTML and PDF,   │
│   highlighting our problem, architecture, RAGAS metrics, and live demo."               │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🧭 The 17 Installed Skills Master Guide

Here is the exact playbook for using every pre-installed skill across the framework's layers:

| Skill Name | Target Stack Layer | How Teammates Must Use It | Sample AI Agent Prompt |
| :--- | :--- | :--- | :--- |
| **`fastapi-production-archetype`** | Backend API | Generates production-ready FastAPI routes, lifespan managers, and Pydantic envelopes. | *"Generate a new router in api/v1/endpoints/analytics.py using ResponseEnvelope and async DB dependency."* |
| **`pgvector-hybrid-search`** | Database / Search | Configures HNSW indexes and constructs hybrid cosine + BM25 reciprocal rank fusion queries. | *"Write a hybrid search query matching user query against document_chunks with RRF weighting."* |
| **`fastmcp-tool-server`** | AI / Tooling | Creates typed Model Context Protocol tool endpoints over HTTP Server-Sent Events. | *"Wrap our FFmpeg audio processing script into an isolated FastMCP SSE tool with typed schema."* |
| **`langgraph-production-patterns`** | AI / Agents | Scaffolds cyclic state graphs with checkpoint persistence and human approval interrupt gates. | *"Build a multi-agent supervisor graph that coordinates researcher and writer nodes with interrupt_before gates."* |
| **`agent-security-guardrails`** | AI / Security | Implements prompt injection filters, SQL mutation blockers, and session token budget guards. | *"Add an input guardrail that detects jailbreak patterns and verifies SQL queries are strictly SELECT-only."* |
| **`agent-eval-harness`** | AI / Testing | Runs automated 25-case golden benchmark suites measuring RAGAS Faithfulness and Answer Relevance. | *"Run the eval harness on our RAG pipeline and output a markdown table of Faithfulness scores for our slides."* |
| **`async-agent-celery-redis`** | Backend / Queue | Configures asynchronous task queues, Redis Pub/Sub channels, and SSE status streaming. | *"Set up an async job worker that processes document embeddings and broadcasts progress percent over Redis."* |
| **`rag-reranking-pipeline`** | AI / Retrieval | Implements 2-stage retrieval using FlashRank neural cross-encoders to score candidates in $<20\text{ms}$. | *"Add FlashRank reranking to our retrieval pipeline to narrow top 25 candidate chunks down to the 5 most relevant."* |
| **`llm-gateway-semantic-cache`** | Production Resilience | Configures embedding-based semantic query caching with Redis to return cached responses in $<10\text{ms}$. | *"Implement semantic caching for our query endpoint with a cosine similarity threshold of 0.95."* |
| **`agent-docker-aws-deploy`** | Cloud & DevOps | Generates multi-stage Docker builds, verifies non-root users, and updates AWS ECS Fargate task definitions. | *"Audit our Dockerfile for size optimization and generate an AWS ECS Fargate task definition with ALB routing."* |
| **`context7-docs-fetcher`** | Research & Docs | Fetches current, version-specific library documentation via CLI or MCP tools. | *"Fetch the latest LangGraph 0.2 documentation for AsyncPostgresSaver checkpointer usage."* |
| **`poetry-python-packaging`** | Packaging & Build | Manages Python dependency resolution, package locking, and clean pyproject.toml definitions. | *"Add flashrank and redis dependencies to pyproject.toml and ensure lockfile consistency."* |
| **`hackathon-speedrun-kit`** | Rapid Prototyping | Generates instant synthetic seed data and interactive terminal demo scripts. | *"Create a 3-second database seeding script that populates 50 realistic document chunks with embeddings."* |
| **`marp-presentation-engine`** | Pitch & Presentation | Compiles Markdown presentation notes into high-impact HTML and standalone PDF slide decks. | *"Compile pitch/pitch.marp.md into an HTML slide presentation with dark-mode theme and code highlighting."* |
| **`jev-decision-router`** | AI / Routing | Deploys low-latency System-1 typed classifiers that route requests without consuming slow LLM tokens. | *"Implement a sub-150ms Jev decision router that classifies incoming user intent into RAG, Math, or General."* |
| **`pydantic-ai-workflows`** | AI / Workflows | Authors type-safe Python agent workflows with structured outputs and dependency injection. | *"Create a Pydantic AI agent that parses unstructured PDF invoices into an InvoiceModel schema."* |
| **`hallmark`** | Frontend UI | Enforces anti-AI-slop design constraints, high visual density, clean typography, and muted dark-mode palettes. | *"Refine frontend/index.html to remove generic AI styling, tighten spacing tokens, and add high-contrast badges."* |

---

## 📚 Curated Index of Top Reference Repositories

All official reference repositories integrated into our architecture:

| Repository | GitHub Link | What It Does in Our Framework |
| :--- | :--- | :--- |
| **Marp** | [marp-team/marp](https://github.com/marp-team/marp) | Converts Markdown directly into HTML, PDF, and PPTX pitch decks. |
| **Context7** | [upstash/context7](https://github.com/upstash/context7) | Real-time version-specific documentation fetcher and MCP server. |
| **Pydantic AI** | [pydantic/pydantic-ai](https://github.com/pydantic/pydantic-ai) | Type-safe Python agent framework with dependency injection. |
| **LangGraph** | [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) | Cyclic multi-agent state graphs with persistence and approval gates. |
| **FastMCP** | [jlowin/fastmcp](https://github.com/jlowin/fastmcp) | High-level Python SDK for Model Context Protocol servers over SSE. |
| **FlashRank** | [PrithivirajDamodaran/FlashRank](https://github.com/PrithivirajDamodaran/FlashRank) | Ultra-fast local neural reranker (<20ms) for 2-stage retrieval. |
| **RAGAS** | [explodinggradients/ragas](https://github.com/explodinggradients/ragas) | Retrieval Augmented Generation evaluation metrics (Faithfulness, Relevance). |
| **Promptfoo** | [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) | CLI-based LLM output testing and prompt regression test runner. |
| **ScrapeGraphAI** | [ScrapeGraphAI/Scrapegraph-ai](https://github.com/ScrapeGraphAI/Scrapegraph-ai) | LLM-powered web scraping pipelines for automated data extraction. |
| **Archify** | [tt-a1i/archify](https://github.com/tt-a1i/archify) | Generates interactive SVG architecture diagrams from code evidence. |

---

## 📋 Hackathon Problem Statement Readiness Checklist

Walk through this checklist the moment your team receives the challenge:

- [ ] **1. Is this a deterministic calculation or an AI problem?**
  - If it can be solved with SQL, math, or regex, **do not use an LLM**.
- [ ] **2. Does the task require private documents or dynamic facts?**
  - If YES: Activate the RAG pipeline (`ai_layer/hybrid_retriever.py`).
  - If NO: Use a direct structured prompt (`gpt-4o-mini`).
- [ ] **3. Will the operation take longer than 1 second?**
  - If YES: Route through the async job queue (`backend/src/app/api/v1/endpoints/jobs.py`) and stream progress to the frontend via SSE.
  - If NO: Return the result synchronously.
- [ ] **4. Can the action cause data corruption or financial loss?**
  - If YES: Enforce a Human-in-the-Loop interrupt gate (`ai_layer/langgraph_supervisor.py`).
- [ ] **5. Are external command-line tools needed (FFmpeg, scrapers)?**
  - If YES: Wrap them in FastMCP over SSE (`ai_layer/fastmcp_server.py`). Never use raw shell calls.
- [ ] **6. Have we verified quality with real numbers?**
  - Run the evaluation suite (`python ai_layer/eval_harness.py`) and put the RAGAS Faithfulness score on your pitch slides.

---

## 🎤 Pitch Deck & Stage Demo Playbook

### 1. Generate Your Slide Deck (Marp)
```bash
# Output interactive HTML slides:
node bin/cli.js pitch
# Output standalone PDF presentation:
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

## 🤖 Automated PR Reviewer Agent

Teammates working in branches run the local review agent before pushing or opening pull requests:
```bash
python3 scripts/review_pr.py
```
Checks performed:
* ✔ **Secret Scanning**: Detects accidental API key or credential commits.
* ✔ **SQL Injection Defense**: Verifies queries use parameterized bindings.
* ✔ **Subprocess Isolation**: Verifies shell command isolation.
* ✔ **Ruff Code Formatting**: Enforces PEP 8 and clean imports.

---

## 🏆 Why This Framework Wins Hackathons

1. **Zero Wasted Setup Time**: You skip the first 14 hours of boilerplate setup.
2. **Production Credibility**: Judges see Alembic migrations, HNSW vector indexes, Docker multi-stage builds, and AWS task specs—not fragile toy scripts.
3. **Natural-Fit AI**: The architecture document defends why every AI feature exists with hard metrics, avoiding vanity AI penalties.
4. **Resilient Presentation**: If anything fails on stage, Marp slides and terminal cURL scripts ensure a flawless pitch.

**Built by Sathvik for high-velocity, production-grade hackathon execution.**
