# 🧠 AI Architectural Decision Matrix

> **Core Philosophy**: Never shoehorn AI or complex agent frameworks where standard software engineering solves the problem better, faster, and cheaper. In hackathons, judges penalize "AI for the sake of AI" and reward systems where AI **naturally fits** a real business need.

---

## 1. The Decision Flowchart

```
                            [Feature / Requirement Identified]
                                           │
             ┌─────────────────────────────┴─────────────────────────────┐
             ▼                                                           ▼
   Is the input/output fully                                   Is there ambiguity, natural language,
   structured or deterministic?                                or complex multi-step reasoning?
             │                                                           │
             ▼                                                           ▼
   [DO NOT USE AI]                                             [AI CONSIDERATION]
   • Use PostgreSQL queries                                              │
   • Use regex / standard Python code                                   │
   • Latency: 2ms | Cost: $0.00                                          │
                                                                         │
                 ┌───────────────────────────────────────────────────────┴───────────────────┐
                 ▼                                                                           ▼
      Does it need dynamic external                                              Is it a standard task
      knowledge or private documents?                                            requiring consistent formatting?
                 │                                                                           │
                 ▼                                                                           ▼
           [USE RAG]                                                              [USE FAST LLM PROMPT]
           • pgvector + RRF Hybrid Search                                         • gpt-4o-mini / Haiku
           • When: Domain manuals, PDF Q&A, fresh facts                           • Structured Pydantic outputs
                                                                                  • Latency: 300ms | Cost: Minimal
                                                                                             │
                                                                                             ▼
                                                                           Does the task require MULTIPLE
                                                                           STEPS, EXTERNAL TOOLS, or APPROVALS?
                                                                                             │
                                                                                             ▼
                                                                                   [USE LANGGRAPH / MCP]
                                                                                   • Multi-agent supervisor
                                                                                   • Human-in-the-loop gate
                                                                                   • FastMCP tool isolation
```

---

## 2. Technology Selection Matrix

| Problem Scenario | Best-Fit Technology | Anti-Pattern to Avoid | Why |
| :--- | :--- | :--- | :--- |
| **Simple Data Lookup / Filtering** | Pure SQL / SQLAlchemy | Vector Search (pgvector) | SQL is $1000\times$ faster, exact, and handles numeric ranges deterministically. |
| **Document Q&A with Citations** | **pgvector + RRF Hybrid Search** | Prompt-stuffing all documents | RAG retrieves only relevant chunks, preventing context window overflow and hallucination. |
| **Repetitive / Paraphrased Queries** | **Redis Semantic Cache** | Repeated LLM API calls | Vector caching answers semantically equivalent queries in **8ms at $0.00 cost**. |
| **Multi-Step Tool Workflow** | **LangGraph Supervisor** | Monolithic prompt chain | Breaks the workflow into isolated worker nodes; failed nodes can be retried independently. |
| **High-Risk Operations (Writes/Payments)** | **LangGraph Human-in-the-Loop** | Autonomous execution | Interrupt gate pauses execution for human verification before irreversible actions. |
| **External Command Execution (FFmpeg/APIs)**| **FastMCP Server (SSE)** | Direct `subprocess.run(shell=True)` | FastMCP enforces typed Pydantic schemas, isolated sandboxes, and streaming logs. |
| **Fast Agent Routing (<150ms)** | **Jev / System-One Decision** | Generative GPT-4o supervisor | Non-generative decision engines return typed routing choices in 80ms without waiting for token decoding. |

---

## 3. The 3 Golden Rules for Hackathons

1. **Rule of Groundedness**: If an LLM cannot cite where it found an answer, it does not belong in production. Always ground answers with chunk IDs and confidence scores.
2. **Rule of Least Privilege**: Give the agent read-only database permissions. Never grant `DELETE` or `DROP` capabilities.
3. **Rule of Graceful Degradation**: Always design a fallback. If the primary LLM provider times out or hits a rate limit, cascade to a secondary model or a deterministic error payload.
