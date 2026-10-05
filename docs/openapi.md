# 📜 OpenAPI 3.1 Contract Specification & Tooling Guide

This repository publishes a first-class, standard **OpenAPI 3.1.0** contract that formalizes every API boundary, data envelope, validation constraint, and endpoint response.

> **OpenAPI Reference**: [OpenAPI Specs: Standard tools for OpenAPI contracts can be explored through the OAI/OpenAPI-Specification GitHub Repository](https://github.com/OAI/OpenAPI-Specification).

---

## 📁 Contract Artifacts in this Repository

| Artifact Path | Format | Description |
| :--- | :--- | :--- |
| [`docs/openapi.json`](file:///Users/k.sathvik/.gemini/antigravity/scratch/hackathon-strategy-framework/docs/openapi.json) | JSON (Indented) | Machine-readable OpenAPI 3.1.0 schema for SDK code generation and CI schema validators. |
| [`docs/openapi.yaml`](file:///Users/k.sathvik/.gemini/antigravity/scratch/hackathon-strategy-framework/docs/openapi.yaml) | YAML | Human-readable specification ideal for Git diff review and contract linting. |

---

## 🌐 Interactive Documentation

When the backend is running (`./init.sh` or `uvicorn src.app.main:app`), interactive API explorers are served natively:

- **Swagger UI (Interactive Playground)**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc (Clean Technical Reference)**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **Live OpenAPI JSON Stream**: [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)

---

## 🛠️ Client SDK Generation Workflows

Standard OpenAPI tooling from the ecosystem allows immediate typed client generation:

### 1. TypeScript / React / Next.js Client
Generate strictly typed TypeScript interfaces directly from the contract:
```bash
# Generate TypeScript types
npx openapi-typescript docs/openapi.yaml -o frontend/api-schema.d.ts

# Or generate a complete fetch-based SDK client
npx @openapitools/openapi-generator-cli generate \
  -i docs/openapi.yaml \
  -g typescript-fetch \
  -o frontend/sdk
```

### 2. Python Client SDK
Generate a fully typed Python client using `httpx` and `pydantic`:
```bash
pip install openapi-python-client
openapi-python-client generate --path docs/openapi.yaml --output-path client-python
```

### 3. Local Mock Server (Zero-Backend Frontend Dev)
Frontend teammates can develop against an exact contract mock before backend endpoints are built:
```bash
npx @stoplight/prism-cli mock docs/openapi.yaml -p 4010
# Mock server now live on http://localhost:4010 returning conforming sample payloads
```

---

## 🔄 Re-generating Schema Contracts

Whenever backend endpoints, models, or Pydantic schemas change, update the contract files:
```bash
PYTHONPATH=backend python3 -c "
import json, yaml
from src.app.main import app
schema = app.openapi()
with open('docs/openapi.json', 'w') as f:
    json.dump(schema, f, indent=2)
with open('docs/openapi.yaml', 'w') as f:
    yaml.dump(schema, f, sort_keys=False)
print('OpenAPI contracts synchronized successfully.')
"
```
