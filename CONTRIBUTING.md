# 🤝 Contributing to Hackathon Strategy Framework (HSF)

Welcome to the team! This repository follows professional, production-grade engineering practices inspired by the top open-source repositories (FastAPI, LangGraph, Supabase).

---

## 🚀 Teammate Workflow in 5 Steps

### 1. Branch Strategy
Always create a dedicated feature branch from `main`:
```bash
git checkout -b feat/your-feature-name
```
Branch naming conventions:
- `feat/*`: New features, endpoints, or UI views
- `fix/*`: Bug fixes or security patches
- `docs/*`: Architecture documentation or OpenAPI updates
- `test/*`: Evaluation harness and test additions

### 2. Environment Setup
```bash
# Make scripts executable and launch local dependencies
chmod +x init.sh bin/cli.js pitch/generate_pitch.sh pitch/demo.sh
./init.sh
```

### 3. Local Verification Before Commit
Never push untested code. Run the full verification suite locally:
```bash
# 1. Lint and format code with Ruff
ruff check --fix .
ruff format .

# 2. Run unit tests and API checks
PYTHONPATH=backend pytest

# 3. Run the automated PR reviewer agent
python3 scripts/review_pr.py
```

### 4. Conventional Commit Messages
Write clear, structured commit messages:
```bash
git commit -m "feat(api): add document upload and hybrid vector search endpoint"
git commit -m "fix(security): sanitize prompt injection keywords in RAG retriever"
```

### 5. Pull Request Submission
Open a PR against `main` using our standard [Pull Request Template](.github/pull_request_template.md). Ensure:
- [x] All automated checks pass (`ci.yml` and `pr-reviewer-agent.yml`).
- [x] No raw database strings or hardcoded API keys are included.
- [x] API changes adhere to the OpenAPI 3.1 specification in `docs/openapi.json`.

---

## 🛡️ Code Quality Standards

* **Type Safety**: All backend inputs and outputs must use Pydantic v2 schemas.
* **Database Isolation**: Never bypass Row-Level Security (RLS) policies.
* **Resilience**: Any call to external AI APIs must use `@retry_with_exponential_backoff` and Circuit Breakers.
* **Zero AI Slop**: Frontend UI must use tokenized dark-mode CSS and responsive layouts without generic placeholders.
