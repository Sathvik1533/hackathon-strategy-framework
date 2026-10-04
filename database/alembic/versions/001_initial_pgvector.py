"""001_initial_pgvector

Revision ID: 001_initial_pgvector
Revises:
Create Date: 2026-10-04 23:00:00.000000

"""

import sqlalchemy as sa
from alembic import op
from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects.postgresql import TSVECTOR

# revision identifiers, used by Alembic.
revision = "001_initial_pgvector"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Enable pgvector extension
    op.execute("CREATE EXTENSION IF NOT EXISTS vector;")

    # 2. Create document_chunks table
    op.create_table(
        "document_chunks",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("title", sa.String(length=255), nullable=True),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("source", sa.String(length=255), nullable=True, server_default="manual"),
        sa.Column("embedding", Vector(1536), nullable=False),
        sa.Column(
            "tsv_content",
            TSVECTOR,
            sa.Computed("to_tsvector('english', content)", persisted=True),
            nullable=False,
        ),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
        ),
    )

    # 3. Create HNSW Cosine Index
    op.execute("""
        CREATE INDEX idx_doc_chunks_hnsw 
        ON document_chunks 
        USING hnsw (embedding vector_cosine_ops)
        WITH (m = 16, ef_construction = 64);
    """)

    # 4. Create Full-Text GIN Index
    op.create_index(
        "idx_doc_chunks_tsv", "document_chunks", ["tsv_content"], postgresql_using="gin"
    )


def downgrade() -> None:
    op.drop_table("document_chunks")
    op.execute("DROP EXTENSION IF EXISTS vector;")
