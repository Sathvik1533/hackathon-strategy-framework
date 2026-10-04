from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

async def hybrid_rrf_search(
    session: AsyncSession,
    query_text: str,
    query_embedding: List[float],
    limit: int = 10,
    rrf_k: int = 60
) -> List[Dict[str, Any]]:
    """
    Executes dense vector search and sparse full-text search in PostgreSQL,
    combining rankings via Reciprocal Rank Fusion (RRF).
    """
    raw_sql = text("""
    WITH vector_matches AS (
        SELECT 
            id,
            title,
            content,
            ROW_NUMBER() OVER (ORDER BY embedding <=> CAST(:vector AS vector)) AS rank
        FROM document_chunks
        ORDER BY embedding <=> CAST(:vector AS vector)
        LIMIT 25
    ),
    keyword_matches AS (
        SELECT 
            id,
            title,
            content,
            ROW_NUMBER() OVER (ORDER BY ts_rank_cd(tsv_content, plainto_tsquery('english', :query)) DESC) AS rank
        FROM document_chunks
        WHERE tsv_content @@ plainto_tsquery('english', :query)
        ORDER BY ts_rank_cd(tsv_content, plainto_tsquery('english', :query)) DESC
        LIMIT 25
    )
    SELECT 
        COALESCE(v.id, k.id) AS id,
        COALESCE(v.title, k.title) AS title,
        COALESCE(v.content, k.content) AS content,
        COALESCE(1.0 / (:rrf_k + v.rank), 0.0) + 
        COALESCE(1.0 / (:rrf_k + k.rank), 0.0) AS rrf_score
    FROM vector_matches v
    FULL OUTER JOIN keyword_matches k ON v.id = k.id
    ORDER BY rrf_score DESC
    LIMIT :limit;
    """)

    result = await session.execute(
        raw_sql,
        {
            "vector": str(query_embedding),
            "query": query_text,
            "rrf_k": rrf_k,
            "limit": limit
        }
    )

    return [
        {
            "id": row.id,
            "title": row.title,
            "content": row.content,
            "score": float(row.rrf_score)
        }
        for row in result.fetchall()
    ]
