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


@pytest.mark.asyncio
async def test_agent_orchestrate_squad(async_client):
    # Test 1-person Solo Pioneer
    res1 = await async_client.post(
        "/api/v1/agent/orchestrate-squad",
        json={"problem_statement": "Automated Logistics Delivery Drone Routing", "team_size": 1},
    )
    assert res1.status_code == 200
    data1 = res1.json()["data"]
    assert data1["team_size"] == 1
    assert "Solo Pioneer" in data1["team_strategy_archetype"]
    assert len(data1["teammate_assignments"]) == 1
    assert "Orbit Prime" in data1["teammate_assignments"][0]["companion_robot"]["codename"]
    assert len(data1["robot_squad"]) == 6

    # Test 3-person Trio Strike Team
    res3 = await async_client.post(
        "/api/v1/agent/orchestrate-squad",
        json={"problem_statement": "Real-time Fraud Detection Payment Gateway", "team_size": 3},
    )
    assert res3.status_code == 200
    data3 = res3.json()["data"]
    assert data3["team_size"] == 3
    assert "Trio Strike Team" in data3["team_strategy_archetype"]
    assert len(data3["teammate_assignments"]) == 3
    assert data3["features_menu"]["frontend_menu"] is not None
    assert data3["features_menu"]["backend_menu"] is not None

    # Test 5-person Pentad
    res5 = await async_client.post(
        "/api/v1/agent/orchestrate-squad",
        json={"problem_statement": "AI Healthcare Clinical Trials Engine", "team_size": 5},
    )
    assert res5.status_code == 200
    data5 = res5.json()["data"]
    assert data5["team_size"] == 5
    assert len(data5["teammate_assignments"]) == 5
    assert "Mirage" in data5["teammate_assignments"][0]["companion_robot"]["codename"]
    assert "Ironhide" in data5["teammate_assignments"][1]["companion_robot"]["codename"]
    assert "Wheeljack" in data5["teammate_assignments"][2]["companion_robot"]["codename"]
    assert "Ratchet" in data5["teammate_assignments"][3]["companion_robot"]["codename"]
    assert "Bumblebee" in data5["teammate_assignments"][4]["companion_robot"]["codename"]


@pytest.mark.asyncio
async def test_agent_features_menu(async_client):
    res = await async_client.post(
        "/api/v1/agent/features-menu",
        json={"problem_statement": "Decentralized Renewable Energy Carbon Credit Trading"},
    )
    assert res.status_code == 200
    data = res.json()["data"]
    assert "frontend_menu" in data
    assert "backend_menu" in data
    assert "database_menu" in data
    assert "ai_agentic_menu" in data
    assert "devops_cloud_menu" in data
    assert len(data["backend_menu"]["core_features"]) >= 4
    assert len(data["database_menu"]["core_features"]) >= 3


@pytest.mark.asyncio
async def test_agent_skills_endpoints(async_client):
    # List skills
    list_res = await async_client.get("/api/v1/agent/skills")
    assert list_res.status_code == 200
    list_data = list_res.json()["data"]
    assert list_data["total_skills"] >= 10

    # Fetch built-in skill
    fetch_builtin = await async_client.post(
        "/api/v1/agent/skills/fetch",
        json={"skill_identifier": "fastapi-production-archetype", "knowledge_level": "Beginner"},
    )
    assert fetch_builtin.status_code == 200
    data_builtin = fetch_builtin.json()["data"]
    assert data_builtin["skill"]["name"] == "fastapi-production-archetype"
    assert "shaped_instructions" in data_builtin
    assert "Step 1:" in data_builtin["shaped_instructions"]

    # Dynamically fetch / synthesize external skill (e.g., temporal-workflows)
    fetch_external = await async_client.post(
        "/api/v1/agent/skills/fetch",
        json={
            "skill_identifier": "temporal-workflows-orchestration",
            "target_layer": "Backend Resilience",
            "knowledge_level": "Advanced",
        },
    )
    assert fetch_external.status_code == 200
    data_external = fetch_external.json()["data"]
    assert data_external["skill"]["is_dynamically_acquired"] is True
    assert "best_practices" in data_external["skill"]
    assert len(data_external["skill"]["best_practices"]) > 0


@pytest.mark.asyncio
async def test_agent_telemetry_traces_and_memory(async_client):
    # 1. Log a trace
    log_res = await async_client.post(
        "/api/v1/agent/traces/log",
        json={
            "teammate_name": "Devin",
            "role": "Backend Lead",
            "active_branch": "feat/payment-routes",
            "action_type": "CODE_REVIEW",
            "query_or_task": "Reviewed stripe webhook handler with idempotency check",
            "guidance_rendered": "Confirmed distributed lock prevents duplicate charges",
            "detected_risks": ["Ensure webhook secret signature is verified"],
            "outcome_status": "RESOLVED",
        },
    )
    assert log_res.status_code == 200
    log_data = log_res.json()["data"]
    assert log_data["teammate_name"] == "Devin"
    assert "trace_id" in log_data

    # 2. Get recent traces
    traces_res = await async_client.get("/api/v1/agent/traces?limit=10")
    assert traces_res.status_code == 200
    traces_data = traces_res.json()["data"]
    assert traces_data["total_traces"] >= 1
    assert any(t["teammate_name"] == "Devin" for t in traces_data["traces"])

    # 3. Get memory summary
    mem_res = await async_client.get("/api/v1/agent/memory")
    assert mem_res.status_code == 200
    mem_data = mem_res.json()["data"]
    assert "total_interactions" in mem_data
    assert "system_health_index" in mem_data
    assert "devin" in mem_data["teammates_tracked"]
