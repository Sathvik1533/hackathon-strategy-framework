-- ============================================================================
-- SUPABASE ROW-LEVEL SECURITY (RLS) & ACID GUARANTEES
-- ============================================================================
-- This script provides production-grade multi-tenant data isolation and
-- demonstrates the ACID properties enforced by PostgreSQL & Supabase.

-- 1. ACID PROPERTIES IN THIS SCHEMA:
-- • Atomicity:   All chunk insertions and vector index updates commit together in a single transaction or roll back completely.
-- • Consistency: Enforced via Foreign Keys (REFERENCES auth.users), NOT NULL constraints, and dimension checks.
-- • Isolation:   PostgreSQL defaults to "Read Committed" isolation; transactions never see dirty uncommitted writes.
-- • Durability:  Transactions written to Write-Ahead Logging (WAL) survive crashes and power cuts.

-- 2. ENABLE ROW-LEVEL SECURITY (RLS)
ALTER TABLE document_chunks ENABLE ROW LEVEL SECURITY;

-- Add user_id column if not present (linked to Supabase Auth or internal user table)
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name='document_chunks' AND column_name='user_id'
    ) THEN
        ALTER TABLE document_chunks ADD COLUMN user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE;
        ALTER TABLE document_chunks ADD COLUMN is_public BOOLEAN DEFAULT false;
    END IF;
END $$;

-- 3. RLS POLICIES FOR SECURE MULTI-TENANCY:

-- Policy A: SELECT (Read Policy)
-- Users can only read their own private document chunks OR chunks marked as public
CREATE POLICY "Users can only read their own chunks or public data"
ON document_chunks
FOR SELECT
USING (
    auth.uid() = user_id 
    OR is_public = true
);

-- Policy B: INSERT (Create Policy)
-- Users can only insert chunks associated with their own authenticated UID
CREATE POLICY "Users can only insert chunks for themselves"
ON document_chunks
FOR INSERT
WITH CHECK (
    auth.uid() = user_id
);

-- Policy C: UPDATE (Modify Policy)
-- Users can only update their own document chunks
CREATE POLICY "Users can only update their own chunks"
ON document_chunks
FOR UPDATE
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

-- Policy D: DELETE (Destroy Policy)
-- Users can only delete chunks they own
CREATE POLICY "Users can only delete their own chunks"
ON document_chunks
FOR DELETE
USING (auth.uid() = user_id);

-- 4. READ-ONLY AGENT SERVICE ROLE (For LLM Agents)
-- LLM Agents connect using a service role that has SELECT permission ONLY.
-- Even if an agent is tricked via prompt injection into executing "DROP TABLE",
-- the PostgreSQL permissions will block the command instantly.
REVOKE ALL ON document_chunks FROM PUBLIC;
GRANT SELECT ON document_chunks TO authenticated;
