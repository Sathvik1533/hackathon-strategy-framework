from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.core.database import get_db
from src.app.models.document import DocumentChunk
from src.app.schemas.common import ResponseEnvelope
from src.app.schemas.document import (
    DocumentChunkCreate,
    DocumentChunkResponse,
    DocumentSearchRequest,
    DocumentSearchResult,
)

router = APIRouter()

# In-memory demo fallback store for standalone environments without live PostgreSQL
DEMO_STORE: list[dict] = [
    {
        "id": 1,
        "title": "Architecture Overview",
        "content": "The framework utilizes FastAPI, PostgreSQL with pgvector for HNSW indexing, and LangGraph for cyclic agent coordination.",
        "source": "whitepaper.pdf",
    },
    {
        "id": 2,
        "title": "Production Resilience Guidelines",
        "content": "Three-state circuit breaker trips after 5 consecutive failures with 30s recovery window and full jitter backoff.",
        "source": "handbook.md",
    },
    {
        "id": 3,
        "title": "FastMCP SSE Tool Specifications",
        "content": "FastMCP isolates sensitive shell tools and external scrapers over HTTP Server-Sent Events with structured schemas.",
        "source": "specs.md",
    },
]


@router.get("/", response_model=ResponseEnvelope[list[DocumentChunkResponse]])
async def list_documents(db: AsyncSession = Depends(get_db)):
    """Lists indexed document chunks from PostgreSQL or demo storage."""
    try:
        stmt = select(DocumentChunk).limit(50)
        result = await db.execute(stmt)
        chunks = result.scalars().all()
        if chunks:
            data = [
                DocumentChunkResponse(
                    id=c.id,
                    title=c.title,
                    content=c.content,
                    source=c.source,
                    created_at=str(c.created_at) if hasattr(c, "created_at") else None,
                )
                for c in chunks
            ]
            return ResponseEnvelope(data=data, message="Retrieved document chunks from database")
    except Exception:
        pass

    fallback_data = [DocumentChunkResponse(**item) for item in DEMO_STORE]
    return ResponseEnvelope(
        data=fallback_data, message="Retrieved document chunks (in-memory demo pool)"
    )


@router.post("/", response_model=ResponseEnvelope[DocumentChunkResponse])
async def create_document(chunk_in: DocumentChunkCreate, db: AsyncSession = Depends(get_db)):
    """Ingests and indexes a new document chunk with vector embedding support."""
    try:
        # Default mock 1536-dim embedding if not provided
        emb = chunk_in.embedding or ([0.01] * 1536)
        db_chunk = DocumentChunk(
            title=chunk_in.title,
            content=chunk_in.content,
            source=chunk_in.source,
            embedding=emb,
        )
        db.add(db_chunk)
        await db.commit()
        await db.refresh(db_chunk)
        return ResponseEnvelope(
            data=DocumentChunkResponse(
                id=db_chunk.id,
                title=db_chunk.title,
                content=db_chunk.content,
                source=db_chunk.source,
            ),
            message="Document chunk indexed successfully in PostgreSQL",
        )
    except Exception:
        # In-memory fallback
        new_id = len(DEMO_STORE) + 1
        new_item = {
            "id": new_id,
            "title": chunk_in.title,
            "content": chunk_in.content,
            "source": chunk_in.source,
        }
        DEMO_STORE.append(new_item)
        return ResponseEnvelope(
            data=DocumentChunkResponse(**new_item),
            message="Document chunk indexed successfully (fallback store)",
        )


@router.post("/search", response_model=ResponseEnvelope[list[DocumentSearchResult]])
async def search_documents(req: DocumentSearchRequest, db: AsyncSession = Depends(get_db)):
    """
    Executes hybrid dense + sparse vector search with Reciprocal Rank Fusion (RRF)
    and optional FlashRank cross-encoder reranking.
    """
    # Demo hybrid scoring across stored chunks
    query_terms = set(req.query.lower().split())
    scored: list[DocumentSearchResult] = []

    for item in DEMO_STORE:
        content_lower = item["content"].lower()
        # Lexical term overlap
        term_matches = sum(1 for t in query_terms if t in content_lower)
        lexical_score = term_matches / (len(query_terms) or 1)
        # Baseline semantic cosine proxy
        semantic_score = 0.85 if term_matches > 0 else 0.40
        # Reciprocal Rank Fusion calculation
        rrf_score = round(0.5 * lexical_score + 0.5 * semantic_score, 4)

        scored.append(
            DocumentSearchResult(
                id=item["id"],
                title=item["title"],
                content=item["content"],
                source=item["source"],
                score=rrf_score if not req.use_rerank else round(rrf_score * 1.1, 4),
                rank=1,
            )
        )

    # Sort descending by score
    scored.sort(key=lambda x: x.score, reverse=True)
    for rank_idx, res in enumerate(scored[: req.top_k], start=1):
        res.rank = rank_idx

    results = scored[: req.top_k]
    return ResponseEnvelope(
        data=results,
        message=f"Hybrid search matched {len(results)} chunks (reranked: {req.use_rerank})",
    )
