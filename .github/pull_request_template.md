## 📋 Pull Request Description

### What Changed?
Briefly describe the architectural or feature changes introduced in this PR.

### Related Issue / Problem Statement
Closes # [issue number]

---

## 🔍 Pre-Merge Verification Checklist

- [ ] **Type Safety & Contracts**: All inputs and outputs adhere to Pydantic v2 schemas and OpenAPI 3.1 specifications (`docs/openapi.json`).
- [ ] **Security & Guardrails**:
  - [ ] No hardcoded API keys or plaintext secrets.
  - [ ] Database queries use parameterized binding (`:param`).
  - [ ] Supabase Row-Level Security (RLS) policies are honored.
- [ ] **Production Resilience**:
  - [ ] External LLM/API calls wrap with Exponential Backoff + Circuit Breakers.
  - [ ] Asynchronous jobs stream progress events over Redis Pub/Sub (SSE).
- [ ] **Automated Testing & Linting**:
  - [ ] `ruff check .` passes with 0 errors.
  - [ ] `ruff format .` passes.
  - [ ] `PYTHONPATH=backend pytest` passes all tests.
  - [ ] `python3 scripts/review_pr.py` gives **APPROVED FOR MERGE**.

---

## 📸 Screenshots / Demonstration
*Attach terminal cURL output, SSE streaming logs, or UI screenshots.*
