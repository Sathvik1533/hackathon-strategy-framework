from typing import Any

try:
    from flashrank import Ranker, RerankRequest

    ranker = Ranker(model_name="ms-marco-TinyBERT-L-2-v2", cache_dir="/tmp/flashrank")
except Exception:
    ranker = None


def rerank_candidate_chunks(
    query: str, raw_candidates: list[dict[str, Any]], top_n: int = 5
) -> list[dict[str, Any]]:
    """
    Stage 2 Neural Reranker: Takes top 25 broad candidates from pgvector,
    computes cross-attention, and returns top 5 high-precision chunks.
    """
    if not ranker or not raw_candidates:
        return raw_candidates[:top_n]

    passages = [
        {"id": c["id"], "text": c["content"], "meta": {"title": c.get("title", "")}}
        for c in raw_candidates
    ]

    rerank_request = RerankRequest(query=query, passages=passages)
    results = ranker.rerank(rerank_request)

    return [
        {
            "id": r["id"],
            "title": r.get("meta", {}).get("title", ""),
            "content": r["text"],
            "rerank_score": round(float(r["score"]), 4),
        }
        for r in results[:top_n]
    ]
