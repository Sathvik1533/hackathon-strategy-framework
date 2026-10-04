import asyncio
import os
import sys

# Ensure backend path is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from sqlalchemy.ext.asyncio import AsyncSession
from src.app.core.database import AsyncSessionLocal
from src.app.models.document import DocumentChunk

DEMO_RECORDS = [
    {
        "title": "Architecture Standards",
        "content": "All asynchronous agentic jobs must stream progress over Redis Pub/Sub to FastAPI SSE endpoints to prevent thread blocking.",
        "source": "governance_doc"
    },
    {
        "title": "Security Protocol",
        "content": "Database tools exposed to LLM agents must connect via a dedicated read-only Postgres user, strictly forbidding DROP, DELETE, or ALTER operations.",
        "source": "security_whitepaper"
    },
    {
        "title": "Hackathon Strategy",
        "content": "In a 24-hour sprint, allocate hours 0-2 for specification, 2-12 for core implementation, 12-18 for AI layer integration, and 18-24 for evals, pitch deck, and rehearsal.",
        "source": "hackathon_handbook"
    },
    {
        "title": "Hybrid Search Formula",
        "content": "Reciprocal Rank Fusion (RRF) scores candidates as 1.0 / (60 + rank), combining sparse BM25 and dense vector cosine distance without score normalization.",
        "source": "retrieval_architecture"
    },
    {
        "title": "Human-in-the-Loop Safeguard",
        "content": "Irreversible financial, transactional, or file-deletion operations must trigger an interrupt_before checkpoint in LangGraph, pausing for explicit human authorization.",
        "source": "agent_governance"
    }
]

def generate_mock_embedding(dim=1536) -> list[float]:
    import math
    return [math.sin(i * 0.1) * 0.05 for i in range(dim)]

async def seed_database():
    print("🌱 Connecting to PostgreSQL and seeding demo records...")
    async with AsyncSessionLocal() as session:
        for idx, rec in enumerate(DEMO_RECORDS, 1):
            chunk = DocumentChunk(
                title=rec["title"],
                content=rec["content"],
                source=rec["source"],
                embedding=generate_mock_embedding()
            )
            session.add(chunk)
        await session.commit()
    print(f"✅ Successfully seeded {len(DEMO_RECORDS)} production demo records with 1536-dim embeddings!")

if __name__ == "__main__":
    asyncio.run(seed_database())
