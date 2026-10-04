# ☁️ AWS Cloud Production Architecture & Trade-Offs

This guide details how the Hackathon Strategy Framework deploys to **Amazon Web Services (AWS)** using production-grade patterns.

---

## 1. AWS End-to-End Infrastructure Diagram

```
                 [Internet / Users]
                         │
                         ▼
        ┌───────────────────────────────────┐
        │ AWS Application Load Balancer(ALB)│
        │ • HTTPS Termination (ACM SSL)     │
        │ • Health Check Path: /api/v1/health│
        └─────────────────┬─────────────────┘
                          │
            ┌─────────────┴─────────────┐
            ▼                           ▼
 ┌──────────────────────┐    ┌──────────────────────┐
 │ ECS Fargate: API Task│    │ ECS Fargate: Worker  │
 │ • FastAPI Web Service│    │ • Celery / FastMCP   │
 │ • Image from AWS ECR │    │ • Media / LangGraph  │
 └──────────┬───────────┘    └──────────┬───────────┘
            │                           │
            ├─────────────┬─────────────┤
            ▼             ▼             ▼
  ┌────────────────┐ ┌──────────────┐ ┌────────────────┐
  │ Amazon S3      │ │ AWS DynamoDB │ │ Amazon RDS     │
  │ • Raw PDFs     │ │ • Session ID │ │ • PostgreSQL 16│
  │ • Rendered MP4s│ │ • Fast Locks │ │ • pgvector HNSW│
  │ • Eval Reports │ │ • Key-Value  │ │ • ACID Relational│
  └────────────────┘ └──────────────┘ └────────────────┘
```

---

## 2. AWS Services Breakdown: What to Use When

### A. AWS Application Load Balancer (ALB)
* **What it does**: Distributes traffic across container tasks, manages SSL certificates, and handles blue/green zero-downtime deployments.
* **Health Check Setting**:
  - Path: `/api/v1/health`
  - Interval: 30 seconds
  - Healthy threshold: 2 consecutive 200 OKs
  - Unhealthy threshold: 3 failures (drains traffic automatically)

### B. AWS ECS on AWS Fargate (Elastic Container Service)
* **What it does**: Runs your Docker containers without you having to manage EC2 virtual machines.
* **Why Fargate instead of EC2?**: Zero server patching, auto-scales tasks based on CPU/Memory, and isolates container resources cleanly.
* **Task Sizing for Hackathons**:
  - API Container: 1 vCPU, 2GB RAM.
  - Worker Container (FFmpeg / heavy media): 2 vCPU, 4GB RAM.

### C. Amazon ECR (Elastic Container Registry)
* **What it does**: Private, secure Docker image registry.
* **Workflow**: GitHub Actions builds your multi-stage Dockerfile, tags it with the git commit SHA, and pushes to ECR.

### D. Amazon S3 (Simple Storage Service)
* **What it does**: Highly durable object storage for large binary files.
* **When to use S3 vs Database**:
  - **Use S3**: Anything $> 100\text{KB}$ (uploaded PDF documents, rendered videos, audio transcripts, synthetic evaluation datasets).
  - **Use Database**: Metadata, vector embeddings, references, foreign keys, and S3 pre-signed URLs.

### E. Amazon DynamoDB vs. Redis vs. RDS PostgreSQL
* **The Trade-Off Decision Matrix**:

| Feature / Need | Amazon RDS (PostgreSQL + pgvector) | Redis (ElastiCache / Upstash) | Amazon DynamoDB |
| :--- | :--- | :--- | :--- |
| **Primary Use Case** | Relational schemas, complex JOINs, vector embeddings (HNSW). | Sub-10ms semantic cache, task broker, live SSE pub/sub. | High-scale, key-value lookup, serverless session persistence. |
| **Speed** | 5ms – 25ms | **< 2ms** (in-memory) | 4ms – 10ms (SSD) |
| **Query Flexibility** | Full SQL, CTEs, RRF ranking. | Key-based, Sorted Sets, Hashes. | Single-table partition key queries only. |
| **When to pick in Hackathon** | **Default primary database**. Handles both business data & vectors. | **Default broker**. Powers real-time SSE streams and query cache. | Use if problem requires serverless pay-per-request NoSQL. |

---

## 3. Production Deployment Trade-Offs

1. **ECS Fargate vs. AWS Lambda**:
   - *Fargate*: Ideal for FastAPI with long-running agent threads, SSE streaming, and FFmpeg binaries. No 15-minute timeout.
   - *Lambda*: Struggles with WebSocket/SSE long-lived connections and has cold starts of 1–3s on large Python packages.
2. **Managed RDS vs. Dockerized Postgres**:
   - *Hackathon Phase*: Run Postgres + pgvector inside Docker Compose for instant zero-cost local iteration.
   - *Final Cloud Stage*: Deploy to RDS PostgreSQL with `CREATE EXTENSION vector;` for production durability.
