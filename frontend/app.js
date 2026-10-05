document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("jobForm");
  const submitBtn = document.getElementById("submitBtn");
  const taskTypeSelect = document.getElementById("taskType");
  const queryInput = document.getElementById("queryInput");
  const terminalBody = document.getElementById("terminalBody");
  const progressBar = document.getElementById("progressBar");
  const jobStatus = document.getElementById("jobStatus");

  function appendLog(text, className = "") {
    const line = document.createElement("div");
    line.className = `log-line ${className}`;
    const timestamp = new Date().toISOString().split("T")[1].slice(0, 8);
    line.textContent = `[${timestamp}] ${text}`;
    terminalBody.appendChild(line);
    terminalBody.scrollTop = terminalBody.scrollHeight;
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    submitBtn.disabled = true;
    submitBtn.textContent = "Dispatching Job...";
    jobStatus.textContent = "ENQUEUEING";
    jobStatus.style.color = "var(--accent-amber)";
    progressBar.style.width = "5%";

    const payload = {
      task_type: taskTypeSelect.value,
      payload: { query: queryInput.value }
    };

    try {
      appendLog(`POST /api/v1/jobs/render -> Task: ${payload.task_type}`, "system");
      const res = await fetch("/api/v1/jobs/render", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (!res.ok) throw new Error(`HTTP error ${res.status}`);

      const data = await res.json();
      const jobId = data.data.job_id;
      appendLog(`Job successfully enqueued. Tracking ID: ${jobId}`, "system");

      // Subscribe to Server-Sent Events (SSE)
      subscribeToSSE(jobId);

    } catch (err) {
      appendLog(`Error submitting job: ${err.message}`, "log-line");
      submitBtn.disabled = false;
      submitBtn.textContent = "Execute Workflow";
      jobStatus.textContent = "ERROR";
      jobStatus.style.color = "var(--accent-rose)";
    }
  });

  function subscribeToSSE(jobId) {
    jobStatus.textContent = "STREAMING SSE";
    jobStatus.style.color = "var(--accent-blue)";
    const eventSource = new EventSource(`/api/v1/jobs/${jobId}/stream`);

    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        progressBar.style.width = `${data.percent}%`;
        appendLog(`[${data.percent}%] ${data.log}`, data.percent === 100 ? "success" : "");

        if (data.status === "completed") {
          jobStatus.textContent = "COMPLETED";
          jobStatus.style.color = "var(--accent-emerald)";
          if (data.result) {
            appendLog(`Final Result: ${JSON.stringify(data.result)}`, "success");
          }
          eventSource.close();
          submitBtn.disabled = false;
          submitBtn.textContent = "Execute Workflow";
        } else if (data.status === "failed") {
          jobStatus.textContent = "FAILED";
          jobStatus.style.color = "var(--accent-rose)";
          eventSource.close();
          submitBtn.disabled = false;
          submitBtn.textContent = "Execute Workflow";
        }
      } catch (e) {
        appendLog(event.data);
      }
    };

    eventSource.onerror = () => {
      appendLog("SSE connection closed or completed.", "system");
      eventSource.close();
      submitBtn.disabled = false;
      submitBtn.textContent = "Execute Workflow";
    };
  }

  // ========================================================
  // Orbit Mascot Strategy Director Interactivity
  // ========================================================
  const problemStatementInput = document.getElementById("problemStatementInput");
  const strategizeBtn = document.getElementById("strategizeBtn");
  const strategizeSpinner = document.getElementById("strategizeSpinner");
  const mascotResult = document.getElementById("mascotResult");
  const mascotNameTag = document.getElementById("mascotNameTag");
  const domainClassifiedBadge = document.getElementById("domainClassifiedBadge");
  const executiveStrategyText = document.getElementById("executiveStrategyText");
  const pitchHookText = document.getElementById("pitchHookText");
  const advantagesList = document.getElementById("advantagesList");
  const skillsTagsContainer = document.getElementById("skillsTagsContainer");
  const roleTabsContainer = document.getElementById("roleTabsContainer");
  const activeRoleTitle = document.getElementById("activeRoleTitle");
  const activeRoleLayer = document.getElementById("activeRoleLayer");
  const activePromptCode = document.getElementById("activePromptCode");
  const copyPromptBtn = document.getElementById("copyPromptBtn");

  let currentTeammatePrompts = {};

  // Preset buttons handling
  document.querySelectorAll(".preset-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const preset = btn.getAttribute("data-preset");
      if (preset && problemStatementInput) {
        problemStatementInput.value = preset;
        triggerStrategize();
      }
    });
  });

  async function triggerStrategize() {
    if (!problemStatementInput || !strategizeBtn) return;
    const problem = problemStatementInput.value.trim();
    if (!problem) return;

    strategizeBtn.disabled = true;
    if (strategizeSpinner) strategizeSpinner.style.display = "inline";

    try {
      const res = await fetch("/api/v1/agent/strategize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ problem_statement: problem })
      });

      if (!res.ok) throw new Error(`HTTP error ${res.status}`);
      const json = await res.json();
      renderMascotPlan(json.data);
    } catch (err) {
      console.warn("Backend API offline or unreachable, rendering Orbit client plan:", err);
      const fallbackPlan = generateFallbackPlan(problem);
      renderMascotPlan(fallbackPlan);
    } finally {
      strategizeBtn.disabled = false;
      if (strategizeSpinner) strategizeSpinner.style.display = "none";
    }
  }

  function renderMascotPlan(plan) {
    if (!mascotResult) return;
    mascotResult.classList.add("active");

    if (mascotNameTag) mascotNameTag.textContent = plan.mascot_name || "Orbit 🤖🚀";
    if (domainClassifiedBadge) domainClassifiedBadge.textContent = plan.domain_classified || "General Intelligence";
    if (executiveStrategyText) executiveStrategyText.textContent = plan.executive_strategy || "";
    if (pitchHookText) pitchHookText.textContent = plan.stage_pitch_hook || "";

    // Advantages
    if (advantagesList) {
      advantagesList.innerHTML = "";
      (plan.competitive_advantage_vs_peers || []).forEach((adv) => {
        const li = document.createElement("li");
        li.textContent = adv;
        advantagesList.appendChild(li);
      });
    }

    // Skills
    if (skillsTagsContainer) {
      skillsTagsContainer.innerHTML = "";
      (plan.skills_activated || []).forEach((skill) => {
        const span = document.createElement("span");
        span.className = "skill-tag";
        span.textContent = `⚡ ${skill}`;
        skillsTagsContainer.appendChild(span);
      });
    }

    // Role Prompts
    currentTeammatePrompts = plan.teammate_prompts || {};
    const roles = Object.keys(currentTeammatePrompts);
    if (roleTabsContainer && roles.length > 0) {
      roleTabsContainer.innerHTML = "";
      roles.forEach((roleKey, idx) => {
        const roleData = currentTeammatePrompts[roleKey];
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = `role-tab-btn ${idx === 0 ? "active" : ""}`;
        btn.textContent = roleData.role_title || roleKey;
        btn.addEventListener("click", () => {
          document.querySelectorAll(".role-tab-btn").forEach((b) => b.classList.remove("active"));
          btn.classList.add("active");
          displayRolePrompt(roleKey);
        });
        roleTabsContainer.appendChild(btn);
      });
      displayRolePrompt(roles[0]);
    }
  }

  function displayRolePrompt(roleKey) {
    const data = currentTeammatePrompts[roleKey];
    if (!data) return;
    if (activeRoleTitle) activeRoleTitle.textContent = data.role_title;
    if (activeRoleLayer) activeRoleLayer.textContent = `Target Layer: ${data.target_layer}`;
    if (activePromptCode) activePromptCode.textContent = data.custom_agent_prompt;
  }

  if (copyPromptBtn) {
    copyPromptBtn.addEventListener("click", async () => {
      if (!activePromptCode) return;
      try {
        await navigator.clipboard.writeText(activePromptCode.textContent);
        const originalText = copyPromptBtn.textContent;
        copyPromptBtn.textContent = "✅ Copied to Clipboard!";
        copyPromptBtn.style.background = "var(--accent-emerald)";
        copyPromptBtn.style.color = "#000";
        setTimeout(() => {
          copyPromptBtn.textContent = originalText;
          copyPromptBtn.style.background = "";
          copyPromptBtn.style.color = "";
        }, 2000);
      } catch (e) {
        console.error("Clipboard copy failed:", e);
      }
    });
  }

  if (strategizeBtn) {
    strategizeBtn.addEventListener("click", triggerStrategize);
  }

  function generateFallbackPlan(problem) {
    return {
      mascot_name: "Orbit 🤖🚀",
      problem_statement: problem,
      domain_classified: "Autonomous System & Domain Intelligence",
      executive_strategy: `Orbit mapped '${problem}' strictly to HSF's pre-configured 7 layers: FastAPI asynchronous endpoints, PostgreSQL 16 + pgvector HNSW hybrid retrieval, Redis multi-pool caching, LangGraph supervisor state graphs, FastMCP SSE tool integration, and Marp presentation slides.`,
      competitive_advantage_vs_peers: [
        "Minute 1 Live Velocity: Full stack running before competitors complete Docker setup.",
        "Zero Fragile Sync Chaining: Async Redis worker queue + SSE streaming eliminates HTTP 504 timeouts.",
        "Precision Grounding: Reciprocal Rank Fusion + FlashRank reranking delivers 94%+ RAGAS accuracy.",
        "Defense-in-Depth Security: Supabase Row Level Security + PyJWT role isolation pre-configured.",
        "Deterministic Pitch Delivery: Marp presentation engine + interactive HTML consoles guarantee stage win."
      ],
      skills_activated: [
        "fastapi-production-archetype",
        "pgvector-hybrid-search",
        "fastmcp-tool-server",
        "langgraph-production-patterns",
        "rag-reranking-pipeline",
        "llm-gateway-semantic-cache",
        "marp-presentation-engine"
      ],
      stage_pitch_hook: `Judges: While rival teams built mock prototypes with brittle LLM calls, our team deployed a zero-trust, hybrid vector retrieval pipeline with sub-12ms cache latencies for '${problem}'.`,
      teammate_prompts: {
        "Lead Architect & Multi-Agent Supervisor": {
          role_title: "Lead Architect & Multi-Agent Supervisor",
          target_layer: "AI Layer (LangGraph State Graph & Agent Dispatcher)",
          custom_agent_prompt: `ROLE: Lead Architect & Multi-Agent Supervisor\nGOAL: Adapt ai_layer/langgraph_supervisor.py for problem: "${problem}".\nSTACK: LangGraph StateGraph, FastMCP tools, Pydantic state.\nSTEPS:\n1. Update AgentState schema in ai_layer/langgraph_supervisor.py.\n2. Ensure human-in-the-loop validation gate before sensitive writes.\n3. Verify test pass with: PYTHONPATH=. pytest.`
        },
        "Frontend Lead (UX & Real-time Console)": {
          role_title: "Frontend Lead (UX & Real-time Console)",
          target_layer: "Frontend Layer (Vanilla SPA, SSE, CSS System)",
          custom_agent_prompt: `ROLE: Frontend Lead (UX & Real-time Console)\nGOAL: Build telemetry and execution cards in frontend/index.html for: "${problem}".\nSTACK: Vanilla JS, Server-Sent Events (SSE), CSS custom properties.\nSTEPS:\n1. Update frontend/index.html to display domain-specific analytics.\n2. Wire EventSource to /api/v1/jobs/{id}/stream.\n3. Validate zero layout shifts and accessibility.`
        },
        "Backend & Tool Platform Lead": {
          role_title: "Backend & Tool Platform Lead",
          target_layer: "Backend & FastMCP Tool Server",
          custom_agent_prompt: `ROLE: Backend & Tool Platform Lead\nGOAL: Expose domain endpoints and FastMCP tools for: "${problem}".\nSTACK: FastAPI, Pydantic V2, Redis connection pool.\nSTEPS:\n1. Create API endpoint under backend/src/app/api/v1/endpoints/.\n2. Add tool to ai_layer/fastmcp_server.py.\n3. Run: ruff check . && ruff format .`
        },
        "AI, Vector & RAG Pipeline Lead": {
          role_title: "AI, Vector & RAG Pipeline Lead",
          target_layer: "Vector & Grounding Pipeline (pgvector + FlashRank)",
          custom_agent_prompt: `ROLE: AI, Vector & RAG Pipeline Lead\nGOAL: Implement hybrid vector search for: "${problem}".\nSTACK: PostgreSQL 16 pgvector HNSW + FlashRank Reranker.\nSTEPS:\n1. Seed domain embeddings in database/seeds/.\n2. Connect RRF fusion search with FlashRank.\n3. Run RAGAS eval test to confirm >90% faithfulness.`
        },
        "DevOps, Cloud & Pitch Lead": {
          role_title: "DevOps, Cloud & Pitch Lead",
          target_layer: "DevOps, Containerization & Pitch Deck",
          custom_agent_prompt: `ROLE: DevOps, Cloud & Pitch Lead\nGOAL: Package production container and compile pitch deck for: "${problem}".\nSTACK: Docker multi-stage, AWS ECS Fargate, Marp presentation engine.\nSTEPS:\n1. Validate infra/Dockerfile build.\n2. Render pitch deck via Marp in pitch/pitch.marp.md.\n3. Verify health checks pass.`
        }
      }
    };
  }
});
