import pytest


@pytest.mark.asyncio
async def test_health_endpoint(async_client):
    response = await async_client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "api_status" in data["data"]


@pytest.mark.asyncio
async def test_auth_login(async_client):
    response = await async_client.post(
        "/api/v1/auth/login",
        json={"email": "developer@hackathon.dev", "password": "secure_password"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "access_token" in data["data"]


@pytest.mark.asyncio
async def test_documents_list_and_create(async_client):
    # List documents
    get_res = await async_client.get("/api/v1/documents/")
    assert get_res.status_code == 200
    get_data = get_res.json()
    assert get_data["success"] is True
    assert isinstance(get_data["data"], list)

    # Create document
    create_payload = {
        "title": "Hackathon Strategy Guide",
        "content": "Rapid prototyping framework with FastAPI, PostgreSQL pgvector, and LangGraph.",
        "source": "guide.md",
    }
    post_res = await async_client.post("/api/v1/documents/", json=create_payload)
    assert post_res.status_code == 200
    post_data = post_res.json()
    assert post_data["success"] is True
    assert post_data["data"]["title"] == "Hackathon Strategy Guide"


@pytest.mark.asyncio
async def test_documents_search(async_client):
    search_payload = {
        "query": "FastAPI PostgreSQL pgvector",
        "top_k": 3,
        "use_rerank": True,
    }
    search_res = await async_client.post("/api/v1/documents/search", json=search_payload)
    assert search_res.status_code == 200
    data = search_res.json()
    assert data["success"] is True
    assert len(data["data"]) > 0
    assert "score" in data["data"][0]


@pytest.mark.asyncio
async def test_analytics_telemetry(async_client):
    res = await async_client.get("/api/v1/analytics/telemetry")
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert data["data"]["ragas_faithfulness"] >= 0.90
    assert "p95_latency_ms" in data["data"]


@pytest.mark.asyncio
async def test_analytics_circuit_breakers(async_client):
    res = await async_client.get("/api/v1/analytics/circuit-breakers")
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert isinstance(data["data"], list)
    assert data["data"][0]["state"] == "CLOSED"


@pytest.mark.asyncio
async def test_agent_query(async_client):
    res = await async_client.post(
        "/api/v1/agent/query",
        json={"query": "What is the vector dimension?", "use_rag": True},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert data["data"]["retrieval_used"] is True


@pytest.mark.asyncio
async def test_agent_strategize(async_client):
    res = await async_client.post(
        "/api/v1/agent/strategize",
        json={"problem_statement": "AI Healthcare Clinical Assistant"},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert "Orbit" in data["data"]["mascot_name"]
    assert "teammate_prompts" in data["data"]
    assert "tech_stack_mapping" in data["data"]
    assert "software_design_pattern" in data["data"]


@pytest.mark.asyncio
async def test_agent_onboard(async_client):
    res = await async_client.post(
        "/api/v1/agent/onboard",
        json={
            "name": "Sarah",
            "role": "Backend API & Resilience Lead",
            "contribution_goal": "Build async streaming SSE routes",
            "knowledge_level": "Intermediate",
            "ai_ide": "Antigravity",
            "active_branch": "feat/backend-api",
            "problem_statement": "Autonomous Logistics Dispatch",
        },
    )
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert "Sarah" in data["data"]["welcome_message"]
    assert "senior_guidance" in data["data"]
    assert len(data["data"]["senior_guidance"]["immediate_actions_what_to_do"]) > 0
    assert len(data["data"]["senior_guidance"]["critical_guardrails_what_not_to_do"]) > 0
    assert "customized_ai_ide_prompt" in data["data"]


@pytest.mark.asyncio
async def test_agent_senior_advice(async_client):
    res = await async_client.post(
        "/api/v1/agent/senior-advice",
        json={
            "name": "David",
            "role": "Database & Vector Search Lead",
            "active_branch": "feat/database-rls",
            "contribution_goal": "Setup pgvector HNSW index",
            "knowledge_level": "Intermediate",
            "ai_ide": "Cursor",
            "query": "Should I use raw SQL or SQLAlchemy models?",
            "code_snippet": "f'SELECT * FROM docs WHERE user = {name}'",
        },
    )
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert "advice" in data["data"]
    assert "code_critique" in data["data"]
    assert "SQL INJECTION RISK" in data["data"]["code_critique"]
    assert len(data["data"]["what_not_to_do"]) > 0


@pytest.mark.asyncio
async def test_agent_pattern_decision(async_client):
    res = await async_client.post(
        "/api/v1/agent/pattern-decision",
        json={"problem_statement": "Real-time IoT drone fleet collision avoidance telemetry"},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert "Event-Driven" in data["data"]["pattern_name"]
    assert "why_chosen" in data["data"]
    assert "why_not_microservices" in data["data"]
    assert "folder_anatomy_implications" in data["data"]
