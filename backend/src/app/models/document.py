from sqlalchemy import Column, Integer, String, Text, Index, Computed
from sqlalchemy.dialects.postgresql import TSVECTOR
from pgvector.sqlalchemy import Vector
from src.app.models.base import TimestampedModel

class DocumentChunk(TimestampedModel):
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=True)
    content = Column(Text, nullable=False)
    source = Column(String(255), nullable=True, default="manual")
    
    # 1536 dimensions for OpenAI / standard embeddings
    embedding = Column(Vector(1536), nullable=False)

    # Generated column for fast PostgreSQL full-text search (BM25 equivalent)
    tsv_content = Column(
        TSVECTOR,
        Computed("to_tsvector('english', content)", persisted=True),
        nullable=False
    )

    __table_args__ = (
        # Production HNSW Cosine Index
        Index(
            "idx_doc_chunks_hnsw",
            "embedding",
            postgresql_using="hnsw",
            postgresql_with={"m": 16, "ef_construction": 64},
            postgresql_ops={"embedding": "vector_cosine_ops"}
        ),
        # GIN index for sparse full-text search
        Index("idx_doc_chunks_tsv", "tsv_content", postgresql_using="gin"),
    )
