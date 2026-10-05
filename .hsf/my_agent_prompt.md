# 🤖 Hackathon Agent Prompt: Backend API & Resilience Lead
**Teammate**: Teammate  
**Companion Autobot**: Ironhide 🛡️⚡ (Backend Titan & Resilience Sentinel)  
**Sprint Problem Statement**: "Autonomous Enterprise Multi-Agent Intelligence System"  
**Assigned Git Branch**: `feat/backend-api`  
**Assigned Layers**: FastAPI Routes, Redis Pool & Rate Limiter, Circuit Breakers  

---

## 🎯 Your Mission & Architectural Contract
You are paired with **Ironhide 🛡️⚡ (Backend Titan & Resilience Sentinel)** in the Hackathon Strategy Framework (HSF).
Your job is to implement production-grade, tested solutions for:
**Autonomous Enterprise Multi-Agent Intelligence System**

### 📁 Your Primary Files to Edit:
- `backend/src/app/api/v1/endpoints/ (Domain routes)`
- `backend/src/app/core/redis.py (Caching & Rate limits)`
- `backend/tests/test_api.py (Unit & Integration tests)`

### 🚫 DO NOT TOUCH (Zero-Collision Rule):
- `frontend/index.html`
- `pitch/pitch.marp.md`

### ⚡ Verification Commands:
```bash
PYTHONPATH=backend pytest (Run 17 test suite)
curl http://localhost:8000/api/v1/health (Verify API)
```

---

## 🧠 Instructions for Your AI IDE (Cursor / Claude Code / Antigravity):
Copy and paste this prompt to your AI assistant:
> "I am Teammate, acting as Backend API & Resilience Lead paired with Ironhide 🛡️⚡ (Backend Titan & Resilience Sentinel) on branch `feat/backend-api`.
> We are solving: 'Autonomous Enterprise Multi-Agent Intelligence System'.
> Strictly respect the zero-collision boundaries. Touch only my assigned files.
> Implement production patterns with full error handling, Pydantic type safety, and unit tests."
