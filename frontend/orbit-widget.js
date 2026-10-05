/**
 * Senior Orbit: Autonomous Desktop & Web Companion Widget
 * (frontend/orbit-widget.js)
 * 
 * Injects a floating senior engineer mascot on any page, maintains
 * teammate onboarding state in localStorage, enforces branch-specific
 * DOs & DON'Ts, and offers live code review & Groq-powered senior advice.
 */

(function () {
  const STORAGE_KEY = "hsf_teammate_profile";
  const GROQ_KEY_STORAGE = "hsf_groq_api_key";

  const SENIOR_TIPS = [
    "👓 Senior Orbit: Never use requests.get() inside async def! Always use httpx.AsyncClient.",
    "👓 Senior Orbit: Remember to run 'python3 scripts/review_pr.py' before opening your PR!",
    "👓 Senior Orbit: Supabase RLS is enabled on all tables. Filter queries by auth.uid().",
    "👓 Senior Orbit: For RAG search, use Reciprocal Rank Fusion (RRF) + FlashRank reranking in <20ms.",
    "👓 Senior Orbit: In a 24h hackathon, avoid microservices. A Modular Monolith + Redis workers ships 5x faster!",
    "👓 Senior Orbit: Emergency stage backup ready? Test 'bash pitch/demo.sh' in your terminal."
  ];

  function getStoredProfile() {
    try {
      const data = localStorage.getItem(STORAGE_KEY);
      return data ? JSON.parse(data) : null;
    } catch (e) {
      return null;
    }
  }

  function saveStoredProfile(profile) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(profile));
    } catch (e) {
      console.error("Failed to save profile to localStorage:", e);
    }
  }

  function getStoredGroqKey() {
    try {
      return localStorage.getItem(GROQ_KEY_STORAGE) || "";
    } catch (e) {
      return "";
    }
  }

  function saveStoredGroqKey(key) {
    try {
      localStorage.setItem(GROQ_KEY_STORAGE, key.trim());
    } catch (e) {
      console.error("Failed to save Groq key:", e);
    }
  }

  // Create and inject HTML elements
  function initWidget() {
    if (document.getElementById("orbitWidgetContainer")) return;

    // 1. Floating Button & Bubble Container
    const container = document.createElement("div");
    container.id = "orbitWidgetContainer";
    container.className = "orbit-floating-container";
    container.innerHTML = `
      <div id="orbitSpeechBubble" class="orbit-speech-bubble">
        👋 Welcome! Click me to onboard and pair with Senior Orbit!
      </div>
      <button type="button" id="orbitFloatingBtn" class="orbit-floating-btn" title="Senior Orbit Engineer Companion">
        <div class="orbit-avatar-pulse">
          <span class="orbit-pulse-ring"></span>
          <span>👓🤖</span>
        </div>
        <div class="orbit-btn-meta">
          <span class="orbit-btn-title">Senior Orbit</span>
          <span id="orbitBtnBranch" class="orbit-btn-branch">Click to Onboard</span>
        </div>
      </button>
    `;
    document.body.appendChild(container);

    // 2. Companion Modal Drawer
    const drawerOverlay = document.createElement("div");
    drawerOverlay.id = "orbitDrawerOverlay";
    drawerOverlay.className = "orbit-drawer-overlay";
    drawerOverlay.innerHTML = `
      <div class="orbit-drawer">
        <div class="orbit-drawer-header">
          <div class="orbit-header-left">
            <div class="orbit-header-avatar">👓🤖</div>
            <div class="orbit-header-title">
              <h3>Senior Orbit • Principal Engineer Desk</h3>
              <p id="orbitHeaderSubtitle">Autonomous Pairing Companion & Code Reviewer</p>
            </div>
          </div>
          <button type="button" id="orbitCloseBtn" class="orbit-close-btn">✕ Close</button>
        </div>

        <div class="orbit-tabs-bar">
          <button type="button" class="orbit-tab active" data-tab="tabSeniorDesk">👓 Senior Desk</button>
          <button type="button" class="orbit-tab" data-tab="tabOnboarding">🤝 Teammate Onboarding</button>
          <button type="button" class="orbit-tab" data-tab="tabDesignPattern">📐 Software Design Pattern</button>
        </div>

        <!-- Tab 1: Senior Desk -->
        <div id="tabSeniorDesk" class="orbit-tab-content active">
          <div id="orbitProfileCard" class="orbit-senior-badge-card">
            <div class="orbit-senior-meta">
              <span id="orbitDeskName" style="font-weight:700; color:#fff;">Pairing with Teammate</span>
              <span id="orbitDeskRole" class="orbit-chip">Backend Lead</span>
              <span id="orbitDeskBranch" class="orbit-chip branch">feat/backend-api</span>
              <span id="orbitDeskIde" class="orbit-chip">Antigravity AI</span>
            </div>
            <p id="orbitDeskMission" style="font-size:0.86rem; color:#cbd5e1; margin:6px 0 0 0;"></p>
          </div>

          <div class="orbit-guidance-grid">
            <div class="orbit-card dos">
              <h4>🎯 What You Must DO Right Now</h4>
              <ul id="orbitDosList">
                <li>Complete your onboarding questionnaire in the Onboarding tab to receive targeted guidance.</li>
              </ul>
            </div>
            <div class="orbit-card donts">
              <h4>⚠️ What NOT To Do (Senior Guardrails)</h4>
              <ul id="orbitDontsList">
                <li>NEVER use requests.get() inside async def route handlers.</li>
                <li>NEVER concatenate raw SQL strings (use parameterized SQLAlchemy bindings).</li>
              </ul>
            </div>
          </div>

          <div class="orbit-prompt-card">
            <div class="orbit-prompt-header">
              <strong style="font-size:0.84rem; color:#fff;">🤖 Your Custom Agentic AI IDE Prompt</strong>
              <button type="button" id="orbitCopyIdePromptBtn" class="orbit-btn" style="padding:5px 12px; font-size:0.75rem;">📋 Copy for AI IDE</button>
            </div>
            <pre id="orbitCustomPromptPre" class="orbit-prompt-pre">Onboard first to generate your custom AI prompt...</pre>
          </div>

          <div class="orbit-chat-box">
            <h4 style="font-size:0.88rem; margin-bottom:10px; display:flex; align-items:center; gap:6px;">
              💬 Ask Senior Orbit (Code Review & Advice)
              <span id="groqBadge" class="orbit-chip" style="font-size:0.65rem; display:none;">⚡ Groq Llama-3.3 Powered</span>
            </h4>
            <div id="orbitChatHistory" class="orbit-chat-history">
              <div class="orbit-msg orbit">
                Senior Orbit ready. Paste a code snippet or ask me: "How should I structure the async streaming endpoint?", "Review this SQL query", or "What tests should I write?"
              </div>
            </div>
            <div class="orbit-field">
              <textarea id="orbitQueryInput" rows="2" placeholder="Ask Senior Orbit or paste a code snippet for instant inspection..."></textarea>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <span id="orbitChatStatus" style="font-size:0.75rem; color:#94a3b8;"></span>
              <button type="button" id="orbitAskBtn" class="orbit-btn" style="padding:7px 16px;">Ask Senior Orbit 👓</button>
            </div>
          </div>
        </div>

        <!-- Tab 2: Teammate Onboarding -->
        <div id="tabOnboarding" class="orbit-tab-content">
          <h3 style="font-size:1.05rem; margin-bottom:8px;">🤝 Teammate Onboarding Questionnaire</h3>
          <p style="font-size:0.82rem; color:#94a3b8; margin-bottom:18px;">
            Tell Senior Orbit about yourself. Orbit will observe your chosen role & branch, tailor all DOs & DON'Ts to your level, and synthesize custom prompts for your AI IDE.
          </p>

          <form id="orbitOnboardingForm">
            <div class="orbit-form-grid">
              <div class="orbit-field">
                <label for="onboardName">Your Name</label>
                <input type="text" id="onboardName" required placeholder="e.g. Alex, Sarah, David" value="Developer">
              </div>
              <div class="orbit-field">
                <label for="onboardRole">Your Assigned Squad Role</label>
                <select id="onboardRole">
                  <option value="Backend API & Resilience Lead">Backend API & Resilience Lead</option>
                  <option value="Database & Vector Search Lead">Database & Vector Search Lead</option>
                  <option value="AI & Multi-Agent Architecture Lead">AI & Multi-Agent Architecture Lead</option>
                  <option value="Frontend Console & Real-Time UX Lead">Frontend Console & Real-Time UX Lead</option>
                  <option value="Cloud DevOps, CI/CD & Pitch / Demo Lead">Cloud DevOps, CI/CD & Pitch / Demo Lead</option>
                </select>
              </div>
            </div>

            <div class="orbit-form-grid">
              <div class="orbit-field">
                <label for="onboardBranch">Active Git Branch</label>
                <input type="text" id="onboardBranch" required placeholder="e.g. feat/backend-api" value="feat/backend-api">
              </div>
              <div class="orbit-field">
                <label for="onboardIde">Your Agentic AI IDE</label>
                <select id="onboardIde">
                  <option value="Google Antigravity">Google Antigravity</option>
                  <option value="Anthropic Claude Code">Anthropic Claude Code</option>
                  <option value="Cursor AI">Cursor AI</option>
                  <option value="Windsurf AI">Windsurf AI</option>
                  <option value="Hero Agent">Hero Agent</option>
                </select>
              </div>
            </div>

            <div class="orbit-form-grid">
              <div class="orbit-field">
                <label for="onboardKnowledge">Stack Knowledge Level</label>
                <select id="onboardKnowledge">
                  <option value="Beginner">Beginner (Explain concepts step-by-step)</option>
                  <option value="Intermediate" selected>Intermediate (Production guidelines & standards)</option>
                  <option value="Advanced">Advanced (High-performance concurrency & low latency)</option>
                  <option value="Senior Specialist">Senior Specialist (Architectural edge cases)</option>
                </select>
              </div>
              <div class="orbit-field">
                <label for="onboardGroqKey">Groq API Key (Optional)</label>
                <input type="password" id="onboardGroqKey" placeholder="gsk_... (Optional for ultra-fast Llama-3.3 live reasoning)">
              </div>
            </div>

            <div class="orbit-field">
              <label for="onboardGoal">What You Want To Contribute (Your Goal)</label>
              <textarea id="onboardGoal" rows="2" placeholder="e.g. Build asynchronous task dispatcher and live SSE stream channel...">Build asynchronous task dispatcher on /api/v1/jobs/render with Redis pub/sub and circuit breaker fallbacks.</textarea>
            </div>

            <div class="orbit-field">
              <label for="onboardProblem">Hackathon Problem Statement</label>
              <input type="text" id="onboardProblem" value="Autonomous Enterprise Intelligence with Real-Time Vector Grounding">
            </div>

            <button type="submit" class="orbit-btn" style="width:100%;">🚀 Save Profile & Pair with Senior Orbit</button>
          </form>
        </div>

        <!-- Tab 3: Software Design Pattern -->
        <div id="tabDesignPattern" class="orbit-tab-content">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; flex-wrap:wrap; gap:8px;">
            <h3 style="font-size:1.05rem; margin:0;">📐 Parent Agent Software Design Pattern Decision</h3>
            <span id="patternBadge" class="orbit-chip" style="background:rgba(52,211,153,0.15); color:var(--orbit-success);">MODULAR MONOLITH + EVENT-DRIVEN WORKERS</span>
          </div>
          <p id="patternWhyChosen" style="font-size:0.86rem; color:#cbd5e1; line-height:1.55; margin-bottom:16px;"></p>

          <div class="orbit-guidance-grid">
            <div class="orbit-card donts">
              <h4>🚫 Why NOT Microservices in 24h?</h4>
              <p id="patternWhyNotMicro" style="font-size:0.82rem; color:#cbd5e1;"></p>
            </div>
            <div class="orbit-card donts">
              <h4>🚫 Why NOT a Simple Monolith Script?</h4>
              <p id="patternWhyNotScript" style="font-size:0.82rem; color:#cbd5e1;"></p>
            </div>
          </div>

          <h4 style="font-size:0.9rem; margin-bottom:10px;">🗂️ Project Directory Anatomy & Rules</h4>
          <div id="patternFolderList" style="display:flex; flex-direction:column; gap:8px;"></div>
        </div>
      </div>
    `;
    document.body.appendChild(drawerOverlay);

    setupWidgetEvents();
    loadActiveProfile();
    startTipRotation();
  }

  function setupWidgetEvents() {
    const floatingBtn = document.getElementById("orbitFloatingBtn");
    const drawerOverlay = document.getElementById("orbitDrawerOverlay");
    const closeBtn = document.getElementById("orbitCloseBtn");
    const tabs = document.querySelectorAll(".orbit-tab");
    const tabContents = document.querySelectorAll(".orbit-tab-content");
    const onboardingForm = document.getElementById("orbitOnboardingForm");
    const askBtn = document.getElementById("orbitAskBtn");
    const queryInput = document.getElementById("orbitQueryInput");
    const copyPromptBtn = document.getElementById("orbitCopyIdePromptBtn");

    // Open/Close
    floatingBtn.addEventListener("click", () => {
      drawerOverlay.classList.add("active");
      document.getElementById("orbitSpeechBubble").classList.remove("active");
    });

    closeBtn.addEventListener("click", () => {
      drawerOverlay.classList.remove("active");
    });

    drawerOverlay.addEventListener("click", (e) => {
      if (e.target === drawerOverlay) drawerOverlay.classList.remove("active");
    });

    // Tab switching
    tabs.forEach((tab) => {
      tab.addEventListener("click", () => {
        tabs.forEach((t) => t.classList.remove("active"));
        tabContents.forEach((c) => c.classList.remove("active"));
        tab.classList.add("active");
        const targetId = tab.getAttribute("data-tab");
        const targetContent = document.getElementById(targetId);
        if (targetContent) targetContent.classList.add("active");
      });
    });

    // Onboarding Form
    onboardingForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const profile = {
        name: document.getElementById("onboardName").value.trim(),
        role: document.getElementById("onboardRole").value,
        active_branch: document.getElementById("onboardBranch").value.trim(),
        ai_ide: document.getElementById("onboardIde").value,
        knowledge_level: document.getElementById("onboardKnowledge").value,
        contribution_goal: document.getElementById("onboardGoal").value.trim(),
        problem_statement: document.getElementById("onboardProblem").value.trim(),
      };

      const groqKey = document.getElementById("onboardGroqKey").value.trim();
      if (groqKey) saveStoredGroqKey(groqKey);

      saveStoredProfile(profile);
      await triggerOnboardApi(profile);
    });

    // Ask Orbit Chat
    askBtn.addEventListener("click", () => handleAskOrbit());
    queryInput.addEventListener("keydown", (e) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        handleAskOrbit();
      }
    });

    // Copy IDE Prompt
    copyPromptBtn.addEventListener("click", async () => {
      const promptPre = document.getElementById("orbitCustomPromptPre");
      if (!promptPre) return;
      try {
        await navigator.clipboard.writeText(promptPre.textContent);
        const originalText = copyPromptBtn.textContent;
        copyPromptBtn.textContent = "✅ Copied to Clipboard!";
        copyPromptBtn.style.background = "var(--orbit-success)";
        copyPromptBtn.style.color = "#000";
        setTimeout(() => {
          copyPromptBtn.textContent = originalText;
          copyPromptBtn.style.background = "";
          copyPromptBtn.style.color = "";
        }, 2000);
      } catch (err) {
        console.error("Clipboard copy failed:", err);
      }
    });
  }

  async function triggerOnboardApi(profile) {
    const statusLabel = document.getElementById("orbitHeaderSubtitle");
    if (statusLabel) statusLabel.textContent = "Synchronizing with Senior Orbit...";

    try {
      const res = await fetch("/api/v1/agent/onboard", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(profile)
      });

      if (!res.ok) throw new Error(`HTTP error ${res.status}`);
      const json = await res.json();
      renderOnboardingBriefing(json.data);
    } catch (err) {
      console.warn("Backend API offline, rendering client-side briefing:", err);
      const fallbackBriefing = generateFallbackBriefing(profile);
      renderOnboardingBriefing(fallbackBriefing);
    } finally {
      if (statusLabel) statusLabel.textContent = `Pairing with ${profile.name} (${profile.active_branch})`;
      // Switch to Senior Desk tab
      document.querySelector('[data-tab="tabSeniorDesk"]').click();
    }
  }

  function renderOnboardingBriefing(data) {
    const p = data.profile;
    const senior = data.senior_guidance;
    const pattern = data.design_pattern_summary;

    // Update Floating Button
    document.getElementById("orbitBtnBranch").textContent = p.active_branch || p.role;

    // Senior Desk Header
    document.getElementById("orbitDeskName").textContent = `Pairing with ${p.name}`;
    document.getElementById("orbitDeskRole").textContent = p.role;
    document.getElementById("orbitDeskBranch").textContent = p.active_branch;
    document.getElementById("orbitDeskIde").textContent = p.ai_ide;
    document.getElementById("orbitDeskMission").textContent = data.personalized_mission || "";

    // DOs & DON'Ts
    const dosList = document.getElementById("orbitDosList");
    dosList.innerHTML = "";
    (senior.immediate_actions_what_to_do || []).forEach((item) => {
      const li = document.createElement("li");
      li.textContent = item;
      dosList.appendChild(li);
    });

    const dontsList = document.getElementById("orbitDontsList");
    dontsList.innerHTML = "";
    (senior.critical_guardrails_what_not_to_do || []).forEach((item) => {
      const li = document.createElement("li");
      li.textContent = item;
      dontsList.appendChild(li);
    });

    // Custom IDE Prompt
    document.getElementById("orbitCustomPromptPre").textContent = data.customized_ai_ide_prompt || "";

    // Design Pattern Tab
    if (pattern) {
      document.getElementById("patternBadge").textContent = pattern.pattern_name.toUpperCase();
      document.getElementById("patternWhyChosen").textContent = pattern.why_chosen || "";
      document.getElementById("patternWhyNotMicro").textContent = pattern.why_not_microservices || "";
      document.getElementById("patternWhyNotScript").textContent = pattern.why_not_simple_monolith || "";

      const folderList = document.getElementById("patternFolderList");
      folderList.innerHTML = "";
      Object.entries(pattern.folder_anatomy_implications || {}).forEach(([folder, desc]) => {
        const item = document.createElement("div");
        item.style.padding = "8px 12px";
        item.style.background = "#080c14";
        item.style.border = "1px solid #1e293b";
        item.style.borderRadius = "6px";
        item.style.fontSize = "0.8rem";
        item.innerHTML = `<strong style="color:var(--orbit-accent); font-family:var(--font-mono, monospace);">${folder}</strong>: <span style="color:#cbd5e1;">${desc}</span>`;
        folderList.appendChild(item);
      });
    }

    // Speech bubble feedback
    showSpeechBubble(`Senior Orbit paired with ${p.name}! Check your Senior Desk for DOs and DON'Ts.`);
  }

  async function handleAskOrbit() {
    const queryInput = document.getElementById("orbitQueryInput");
    const query = queryInput.value.trim();
    if (!query) return;

    const chatHistory = document.getElementById("orbitChatHistory");
    const statusLabel = document.getElementById("orbitChatStatus");
    const groqKey = getStoredGroqKey();
    const profile = getStoredProfile() || {
      name: "Teammate",
      role: "Backend API & Resilience Lead",
      active_branch: "feat/backend-api",
      ai_ide: "Antigravity",
      knowledge_level: "Intermediate",
      contribution_goal: "Build core endpoints"
    };

    // Append User Message
    const userMsg = document.createElement("div");
    userMsg.className = "orbit-msg user";
    userMsg.textContent = query;
    chatHistory.appendChild(userMsg);
    queryInput.value = "";
    chatHistory.scrollTop = chatHistory.scrollHeight;

    statusLabel.textContent = "Senior Orbit is reviewing...";

    try {
      const res = await fetch("/api/v1/agent/senior-advice", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...profile,
          query: query,
          code_snippet: query.includes("\n") ? query : null,
          groq_api_key: groqKey || null
        })
      });

      if (!res.ok) throw new Error(`HTTP error ${res.status}`);
      const json = await res.json();
      const adviceData = json.data;

      // Append Orbit Response
      const orbitMsg = document.createElement("div");
      orbitMsg.className = "orbit-msg orbit";
      let content = adviceData.advice;
      if (adviceData.code_critique) {
        content += `\n\n🔍 Code Review Critique:\n${adviceData.code_critique}`;
      }
      orbitMsg.innerHTML = content.replace(/\n/g, "<br>");
      chatHistory.appendChild(orbitMsg);

      if (adviceData.groq_powered) {
        document.getElementById("groqBadge").style.display = "inline-block";
      }
    } catch (err) {
      console.warn("Backend advice error, answering client-side:", err);
      const orbitMsg = document.createElement("div");
      orbitMsg.className = "orbit-msg orbit";
      orbitMsg.textContent = `Senior Orbit: Focus on branch ${profile.active_branch}. Always ensure async def endpoints use Pydantic models and return ResponseEnvelope[T]. Run 'python3 scripts/review_pr.py' before merging!`;
      chatHistory.appendChild(orbitMsg);
    } finally {
      statusLabel.textContent = "";
      chatHistory.scrollTop = chatHistory.scrollHeight;
    }
  }

  function loadActiveProfile() {
    const profile = getStoredProfile();
    const groqKey = getStoredGroqKey();

    if (groqKey) {
      const keyInput = document.getElementById("onboardGroqKey");
      if (keyInput) keyInput.value = groqKey;
      const badge = document.getElementById("groqBadge");
      if (badge) badge.style.display = "inline-block";
    }

    if (profile) {
      document.getElementById("onboardName").value = profile.name || "";
      document.getElementById("onboardRole").value = profile.role || "Backend API & Resilience Lead";
      document.getElementById("onboardBranch").value = profile.active_branch || "feat/backend-api";
      document.getElementById("onboardIde").value = profile.ai_ide || "Google Antigravity";
      document.getElementById("onboardKnowledge").value = profile.knowledge_level || "Intermediate";
      document.getElementById("onboardGoal").value = profile.contribution_goal || "";
      triggerOnboardApi(profile);
    }
  }

  function showSpeechBubble(text) {
    const bubble = document.getElementById("orbitSpeechBubble");
    if (!bubble) return;
    bubble.textContent = text;
    bubble.classList.add("active");
    setTimeout(() => {
      bubble.classList.remove("active");
    }, 6000);
  }

  function startTipRotation() {
    let index = 0;
    setInterval(() => {
      // Only pop bubble if drawer is closed
      const drawer = document.getElementById("orbitDrawerOverlay");
      if (drawer && !drawer.classList.contains("active")) {
        showSpeechBubble(SENIOR_TIPS[index % SENIOR_TIPS.length]);
        index++;
      }
    }, 45000); // Every 45s
  }

  function generateFallbackBriefing(profile) {
    return {
      profile: profile,
      welcome_message: `Welcome aboard, ${profile.name}! Senior Orbit is pairing with you on ${profile.active_branch}.`,
      personalized_mission: `Deliver '${profile.contribution_goal}' on branch '${profile.active_branch}'.`,
      design_pattern_summary: {
        pattern_name: "Modular Monolith with Event-Driven Background Workers (Redis Pub/Sub)",
        why_chosen: "Combines development velocity of a single repository with the resilience of async worker queues.",
        why_not_microservices: "Microservices introduce distributed tracing, CORS, and deployment latency that kill 24h teams.",
        why_not_simple_monolith: "Single-file scripts block asyncio event loops during heavy LLM or vector calls.",
        folder_anatomy_implications: {
          "frontend/": "Vanilla SPA with zero heavy bundler steps.",
          "backend/": "Layered FastAPI routers, Pydantic schemas, and circuit breakers.",
          "database/": "PostgreSQL 16 + pgvector HNSW index + Supabase RLS policies.",
          "ai_layer/": "LangGraph supervisor state machine and FastMCP tool server."
        }
      },
      senior_guidance: {
        immediate_actions_what_to_do: [
          `Inspect the core files for ${profile.role}.`,
          "Wrap downstream calls in CircuitBreakers and Exponential Backoff.",
          "Verify test suite with PYTHONPATH=. pytest."
        ],
        critical_guardrails_what_not_to_do: [
          "NEVER use requests.get() inside async def route handlers.",
          "NEVER concatenate raw SQL strings.",
          "NEVER bypass Supabase Row-Level Security policies."
        ]
      },
      customized_ai_ide_prompt: `ROLE: ${profile.role}\nIDE: ${profile.ai_ide}\nBRANCH: ${profile.active_branch}\nGOAL: ${profile.contribution_goal}\nFollow all HSF architecture standards and verify with review_pr.py before committing.`
    };
  }

  // Initialize on load
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initWidget);
  } else {
    initWidget();
  }
})();
