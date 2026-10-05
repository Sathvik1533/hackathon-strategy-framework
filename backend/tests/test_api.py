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


@pytest.mark.asyncio
async def test_agent_aesthetic_decisions(async_client):
    # 1. Industrial Brutalism
    res_ind = await async_client.post(
        "/api/v1/agent/aesthetic-decision",
        json={"problem_statement": "Real-time Kubernetes cloud observability telemetry"},
    )
    assert res_ind.status_code == 200
    data_ind = res_ind.json()["data"]
    assert "Industrial Brutalism" in data_ind["aesthetic_name"]
    assert "--bg-canvas" in data_ind["css_design_tokens"]
    assert "JetBrains Mono" in data_ind["css_design_tokens"]["--font-mono"]

    # 2. Neo-Brutalism
    res_neo = await async_client.post(
        "/api/v1/agent/aesthetic-decision",
        json={"problem_statement": "Viral creator economy social shopping app for GenZ"},
    )
    assert res_neo.status_code == 200
    data_neo = res_neo.json()["data"]
    assert "Neo-Brutalism" in data_neo["aesthetic_name"]
    assert "3px solid #000000" in data_neo["css_design_tokens"]["--border-thick"]

    # 3. Glassmorphism
    res_glass = await async_client.post(
        "/api/v1/agent/aesthetic-decision",
        json={
            "problem_statement": "AI Healthcare Clinical Decision and Patient Diagnosis Assistant"
        },
    )
    assert res_glass.status_code == 200
    data_glass = res_glass.json()["data"]
    assert "Glassmorphism" in data_glass["aesthetic_name"]
    assert "blur(16px)" in data_glass["css_design_tokens"]["--backdrop-blur"]

    # 4. Claymorphism
    res_clay = await async_client.post(
        "/api/v1/agent/aesthetic-decision",
        json={
            "problem_statement": "Interactive school math tutor and habit tracker for young kids"
        },
    )
    assert res_clay.status_code == 200
    data_clay = res_clay.json()["data"]
    assert "Claymorphism" in data_clay["aesthetic_name"]
    assert "28px" in data_clay["css_design_tokens"]["--radius-clay"]

    # 5. Skeuomorphism
    res_skeuo = await async_client.post(
        "/api/v1/agent/aesthetic-decision",
        json={"problem_statement": "Virtual audio synthesizer pedal board and DSP studio mixer"},
    )
    assert res_skeuo.status_code == 200
    data_skeuo = res_skeuo.json()["data"]
    assert "Skeuomorphism" in data_skeuo["aesthetic_name"]
    assert "linear-gradient" in data_skeuo["css_design_tokens"]["--surface-metal"]
