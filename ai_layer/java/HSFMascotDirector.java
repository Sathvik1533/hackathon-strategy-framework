package ai_layer.java;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;

/**
 * Orbit: The Autonomous Java Mascot Director & Architectural Context Engine
 * (ai_layer/java/HSFMascotDirector.java)
 *
 * Enterprise-grade Java implementation of Orbit, designed to run in pure JDK 17+
 * without external dependencies. Autonomously ingests any problem statement,
 * evaluates software architecture patterns and frontend aesthetic paradigms,
 * authors deep architectural justification essays, and generates multi-agent
 * squad prompts for Antigravity, Claude, Cursor, and Hero agents.
 */
public class HSFMascotDirector {

    public static final String MASCOT_NAME = "Orbit 🤖👓 (Senior Principal Robotic Director)";
    public static final String FRAMEWORK_VERSION = "HSF v1.0 Production";

    // --- Data Models ---

    public record SoftwarePatternDecision(
        String patternName,
        String architecturalStyle,
        List<String> designPatternsApplied,
        String whyChosen,
        String whyNotMicroservices,
        String whyNotSimpleMonolith,
        Map<String, String> folderAnatomyImplications,
        Map<String, String> recommendedTeamDelegation
    ) {}

    public record FrontendAestheticDecision(
        String aestheticName,
        String visualArchetype,
        List<String> targetEmotions,
        String whyPerfectFit,
        String whyNotAlternatives,
        Map<String, String> cssDesignTokens,
        Map<String, String> tailwindClassesRecipe,
        List<String> motionInteractionRules
    ) {}

    public record SquadMemberPrompt(
        String roleTitle,
        String targetLayer,
        List<String> coreFiles,
        List<String> assignedSkills,
        String promptBody
    ) {}

    public record TeammateProfile(
        String name,
        String role,
        String activeBranch,
        String contributionGoal,
        String knowledgeLevel,
        String aiIde
    ) {}

    public record SeniorGuidance(
        String role,
        String activeBranch,
        String currentMission,
        List<String> immediateActions,
        List<String> criticalGuardrails,
        List<String> codeReviewRules,
        List<String> recommendedFiles,
        List<String> forbiddenAntipatterns,
        String seniorProTip
    ) {}

    // --- Core Logic ---

    public String inferDomain(String problem) {
        String p = problem.toLowerCase();
        if (containsAny(p, "health", "medic", "patient", "clinic", "bio", "pharma", "clinical", "hospital")) {
            return "Healthcare & Clinical Life Sciences";
        } else if (containsAny(p, "fintech", "fraud", "bank", "pay", "money", "loan", "trade", "crypto", "defi")) {
            return "Financial Technology & Risk Intelligence";
        } else if (containsAny(p, "edu", "learn", "tutor", "school", "teach", "student", "math", "kids")) {
            return "Education & Adaptive Gamified Learning";
        } else if (containsAny(p, "supply", "chain", "logist", "cargo", "ship", "warehous", "fleet")) {
            return "Supply Chain & Autonomous Logistics";
        } else if (containsAny(p, "legal", "contract", "compliance", "law", "audit", "governance")) {
            return "LegalTech & Regulatory Governance";
        } else if (containsAny(p, "cyber", "secur", "vulnerab", "threat", "hack", "penetration")) {
            return "Cybersecurity & Autonomous Threat Defense";
        } else if (containsAny(p, "audio", "music", "synth", "sound", "dsp", "instrument", "mixer")) {
            return "Audio Engineering & Digital Signal Processing";
        } else if (containsAny(p, "consumer", "social", "creator", "influencer", "meme", "viral", "genz")) {
            return "Consumer Social & Viral Creator Economy";
        } else if (containsAny(p, "iot", "drone", "sensor", "telemetry", "robot", "stream", "realtime")) {
            return "IoT Telemetry & Autonomous Drone Systems";
        }
        return "Autonomous Enterprise Intelligence";
    }

    public SoftwarePatternDecision decideSoftwarePattern(String problem) {
        String p = problem.toLowerCase();

        if (containsAny(p, "iot", "telemetry", "drone", "fraud", "stream", "sensor", "fleet", "realtime", "event", "traffic")) {
            Map<String, String> folders = new LinkedHashMap<>();
            folders.put("backend/src/app/api/v1/", "Non-blocking command ingestion routes returning HTTP 202 Accepted within 5ms.");
            folders.put("backend/src/app/core/redis.py", "Redis Streams (XADD/XREADGROUP) event bus with pub/sub channel multiplexing.");
            folders.put("backend/src/app/services/", "Domain command handlers enforcing idempotency via Redis SETNX locks.");
            folders.put("ai_layer/", "Background event consumer workers listening on dedicated consumer groups.");
            folders.put("frontend/", "Server-Sent Events (SSE) EventSource consumer updating high-density telemetry.");

            Map<String, String> delegation = new LinkedHashMap<>();
            delegation.put("Backend Lead", "Implement fast ingestion endpoints, validate Pydantic schemas, publish to Redis Streams.");
            delegation.put("Database Lead", "Manage append-only event log schema, hypertable partitioning, and pgvector indexes.");
            delegation.put("AI Lead", "Build asynchronous stream consumers, LangGraph state transition nodes, and FlashRank reranking.");
            delegation.put("Frontend Lead", "Construct zero-latency telemetry stream console with EventSource and terminal log viewer.");
            delegation.put("DevOps Lead", "Configure Redis cluster health checks, multi-stage Docker builds, and ECS task CPU allocation.");

            return new SoftwarePatternDecision(
                "Event-Driven Architecture (EDA) with Asynchronous Redis Streams & CQRS Light",
                "Decoupled Event-Driven Pipeline + Asynchronous Worker Mesh",
                List.of(
                    "CQRS Light (Command/Query Responsibility Segregation)",
                    "Publisher-Subscriber Event Bus (Redis Pub/Sub & Streams)",
                    "Distributed Idempotency Mutex (Redis SETNX)",
                    "Observer Pattern over Server-Sent Events (SSE)"
                ),
                "High-frequency telemetry and sensor streams require instant sub-5ms command acknowledgment without blocking read queries. "
                    + "Decoupling command writes via Redis queues ensures that sudden event bursts never freeze browser responsiveness.",
                "Full microservices introduce distributed network latency, cross-container network routing failures, and distributed tracing "
                    + "complexity that reliably causes teams to run out of time during a 24-hour sprint. A modular event-bus in a single unified codebase "
                    + "delivers the exact same decoupling benefits with zero deployment overhead.",
                "A naive monolithic request/response loop blocks the single-threaded asyncio event loop during prolonged LLM or embedding calls, "
                    + "triggering HTTP 504 Gateway Timeouts during live stage judging.",
                folders,
                delegation
            );
        } else if (containsAny(p, "agent", "tool", "mcp", "doctor", "health", "clinical", "legal", "audit", "compliance", "multi-agent")) {
            Map<String, String> folders = new LinkedHashMap<>();
            folders.put("backend/src/app/core/", "Invariant domain ports (resilience, database session protocols, circuit breakers).");
            folders.put("ai_layer/fastmcp_server.py", "Outbound tool adapter running on isolated port 8001 with strict schema validation.");
            folders.put("ai_layer/langgraph_supervisor.py", "Core multi-agent state supervisor orchestrating specialist subagents.");
            folders.put("database/supabase_rls.sql", "Persistence adapter enforcing multi-tenant isolation and Row-Level Security.");
            folders.put("frontend/", "Real-time human-in-the-loop review modal and streaming execution traces.");

            Map<String, String> delegation = new LinkedHashMap<>();
            delegation.put("Backend Lead", "Design inbound REST ports, Pydantic DTO adapters, and Circuit Breaker policies.");
            delegation.put("Database Lead", "Enforce Postgres repository patterns, Supabase RLS security policies, and vector seeds.");
            delegation.put("AI Lead", "Architect Supervisor state machine, FastMCP tool adapters, and RAGAS faithfulness evals.");
            delegation.put("Frontend Lead", "Implement interactive human-in-the-loop approval gate and live terminal trace viewer.");
            delegation.put("DevOps Lead", "Build multi-stage Docker image, configure AWS ALB health probes, and rehearse pitch demo.");

            return new SoftwarePatternDecision(
                "Modular Monolith with Hexagonal Ports & Adapters + FastMCP Tool Isolation",
                "Hexagonal Architecture (Clean Architecture / Ports & Adapters)",
                List.of(
                    "Ports & Adapters (Hexagonal Architecture)",
                    "Supervisor-Worker Multi-Agent Pattern (LangGraph)",
                    "Human-in-the-Loop Interrupt Gate Pattern",
                    "Repository Pattern with Row-Level Security"
                ),
                "Complex multi-agent reasoning and sensitive domain rules require strict isolation between core business logic, "
                    + "external LLM model providers, and third-party tools. If an external tool or scraper crashes, the isolated adapter catches "
                    + "the fault without corrupting system state.",
                "Splitting every agent and tool into independent microservice containers creates severe version drift, uncoordinated "
                    + "database migrations, and fragile deployment pipelines that waste crucial hackathon hours.",
                "Tightly coupling LLM prompts with direct database queries creates brittle spaghetti code where modifying a single database column "
                    + "breaks agent reasoning nodes across the entire system.",
                folders,
                delegation
            );
        } else {
            Map<String, String> folders = new LinkedHashMap<>();
            folders.put("frontend/", "High-density vanilla SPA views without heavy webpack/npm bundle overhead.");
            folders.put("backend/", "Clear separation of endpoints, models, schemas, and resilience policies.");
            folders.put("database/", "Centralized PostgreSQL 16 schemas, Alembic migrations, and pgvector seeds.");
            folders.put("ai_layer/", "Multi-agent graphs, vector hybrid search, and FastMCP tools.");
            folders.put("infra/", "Multi-stage Dockerfile and cloud task definitions.");

            Map<String, String> delegation = new LinkedHashMap<>();
            delegation.put("Backend Lead", "FastAPI routes, Circuit Breakers, ResponseEnvelopes.");
            delegation.put("Database Lead", "PostgreSQL models, pgvector HNSW indexing, Supabase RLS.");
            delegation.put("AI Lead", "LangGraph state graph, FlashRank reranking, RAGAS evals.");
            delegation.put("Frontend Lead", "Real-time console, SSE log terminal, metrics dashboard.");
            delegation.put("DevOps Lead", "Docker build, AWS Fargate task, Marp pitch slides.");

            return new SoftwarePatternDecision(
                "Modular Monolith with Event-Driven Background Workers (Redis Pub/Sub)",
                "Production-Grade Modular Monolith + Async Worker Mesh",
                List.of(
                    "Modular Monolith (Package by Feature / Layer)",
                    "Producer-Consumer Asynchronous Pipeline",
                    "Reciprocal Rank Fusion (RRF) Hybrid Search",
                    "Resilience Decorators (Circuit Breaker + Exponential Backoff)"
                ),
                "The undisputed gold standard for 24-hour hackathon execution. Combines the rapid development velocity and instantaneous "
                    + "debugging of a single repository with the resilience of decoupled asynchronous background workers.",
                "Microservices are an infamous hackathon trap. Teams spend 14 hours debugging cross-container CORS, networking, and distributed "
                    + "database migrations, presenting a broken demo. A modular monolith wins on velocity and reliability.",
                "Single-file monolithic scripts fail under concurrent user load and cannot stream real-time tokens to the browser.",
                folders,
                delegation
            );
        }
    }

    public FrontendAestheticDecision decideFrontendAesthetic(String problem) {
        String p = problem.toLowerCase();

        // 1. Skeuomorphism
        if (containsAny(p, "audio", "music", "synth", "sound", "instrument", "studio", "knob", "dial", "hardware", "controller", "dsp", "analog", "pedal", "mixing", "equalizer")) {
            Map<String, String> tokens = new LinkedHashMap<>();
            tokens.put("--bg-canvas", "#121418");
            tokens.put("--surface-metal", "linear-gradient(145deg, #252932, #181a20)");
            tokens.put("--surface-inset", "linear-gradient(145deg, #101216, #1c2027)");
            tokens.put("--border-bevel", "1px solid #363c4a");
            tokens.put("--border-inner-recess", "1px solid #0e1014");
            tokens.put("--shadow-embossed", "inset 1px 1px 2px rgba(255,255,255,0.15), inset -1px -1px 3px rgba(0,0,0,0.8), 4px 8px 16px rgba(0,0,0,0.6)");
            tokens.put("--shadow-pressed", "inset 2px 2px 5px rgba(0,0,0,0.9), inset -1px -1px 2px rgba(255,255,255,0.05)");
            tokens.put("--font-display", "'DIN 1451', 'Eurostile', 'SF Pro Text', sans-serif");
            tokens.put("--font-mono", "'Geist Mono', 'JetBrains Mono', monospace");
            tokens.put("--accent-led", "#ff851b");
            tokens.put("--accent-meter", "#00e5ff");

            Map<String, String> tw = new LinkedHashMap<>();
            tw.put("card", "bg-gradient-to-br from-[#252932] to-[#181a20] border border-[#363c4a] rounded-lg shadow-[inset_1px_1px_2px_rgba(255,255,255,0.15),inset_-1px_-1px_3px_rgba(0,0,0,0.8),4px_8px_16px_rgba(0,0,0,0.6)] p-5 text-slate-200");
            tw.put("button_primary", "bg-gradient-to-br from-[#2f3542] to-[#1f2229] active:shadow-[inset_2px_2px_5px_rgba(0,0,0,0.9)] border border-[#3c4454] rounded font-semibold text-amber-400 active:translate-y-[1px] transition-transform duration-100");
            tw.put("dial_bezel", "w-16 h-16 rounded-full bg-gradient-to-br from-[#2f333c] to-[#15171c] shadow-[inset_1px_1px_2px_rgba(255,255,255,0.2),2px_4px_8px_rgba(0,0,0,0.7)] flex items-center justify-center");
            tw.put("status_led", "w-3 h-3 rounded-full bg-amber-500 shadow-[0_0_8px_#ff851b]");

            return new FrontendAestheticDecision(
                "Skeuomorphism (Modern Tactile Hardware & Analog Instrumentation)",
                "Tactile Brushed Metal, Embossed Knobs, Recessed Meters & Analog Hardware",
                List.of("Tactile Precision", "Physical Reliability", "Crafted Engineering", "Sensory Familiarity"),
                "For audio engineering, hardware instrumentation, and DSP controllers, users possess deep muscle memory with physical rotaries, faders, and engraved dials. A modern skeuomorphic interface bridges physical hardware control with digital AI intelligence.",
                "Neo-Brutalism lacks the fine analog gradations required for precision dials. Glassmorphism feels too ethereal for physical switches. Claymorphism looks like a toy and destroys professional studio credibility. Industrial Brutalism is too flat.",
                tokens,
                tw,
                List.of(
                    "Animate only transform (translateY/rotate) and opacity.",
                    "Buttons snap downward by 1.5px on :active with --dur-micro (100ms) cubic-bezier(0.16, 1, 0.3, 1).",
                    "Rotary dials use continuous pointer-lock or mouse wheel with inertia damping.",
                    "Status LEDs crossfade opacity without changing element geometry."
                )
            );
        }

        // 2. Claymorphism
        else if (containsAny(p, "edu", "child", "kid", "school", "tutor", "learn", "student", "habit", "mental", "wellness", "mindful", "calm", "friendly", "gamif")) {
            Map<String, String> tokens = new LinkedHashMap<>();
            tokens.put("--bg-canvas", "#eef2ff");
            tokens.put("--surface-card", "#ffffff");
            tokens.put("--border-clay", "none");
            tokens.put("--radius-clay", "28px");
            tokens.put("--shadow-clay", "inset 4px 4px 8px rgba(255,255,255,0.9), inset -4px -4px 8px rgba(165,180,252,0.35), 10px 20px 30px rgba(99,102,241,0.12)");
            tokens.put("--shadow-clay-btn", "inset 2px 2px 4px rgba(255,255,255,0.8), inset -2px -2px 4px rgba(79,70,229,0.2), 6px 12px 20px rgba(99,102,241,0.2)");
            tokens.put("--font-display", "'Plus Jakarta Sans', 'Quicksand', 'Fredoka', sans-serif");
            tokens.put("--accent-primary", "#6366f1");
            tokens.put("--accent-secondary", "#ec4899");

            Map<String, String> tw = new LinkedHashMap<>();
            tw.put("card", "bg-white rounded-[28px] shadow-[inset_4px_4px_8px_rgba(255,255,255,0.9),inset_-4px_-4px_8px_rgba(165,180,252,0.35),10px_20px_30px_rgba(99,102,241,0.12)] p-6 text-slate-800");
            tw.put("button_primary", "bg-indigo-500 text-white rounded-full font-bold px-6 py-3 shadow-[inset_2px_2px_4px_rgba(255,255,255,0.8),inset_-2px_-2px_4px_rgba(79,70,229,0.2),6px_12px_20px_rgba(99,102,241,0.25)] hover:scale-[1.03] active:scale-[0.96] transition-transform duration-200");
            tw.put("badge", "bg-pink-100 text-pink-700 font-semibold px-4 py-1.5 rounded-full shadow-[inset_1px_1px_2px_rgba(255,255,255,0.8)]");
            tw.put("input", "bg-indigo-50/50 rounded-2xl p-4 shadow-[inset_2px_2px_5px_rgba(165,180,252,0.3)] focus:outline-none focus:ring-2 focus:ring-indigo-400");

            return new FrontendAestheticDecision(
                "Claymorphism (Friendly 3D Volumetric Soft Aesthetic)",
                "Pillowy Rounded Cards, Dual Inner Inset Shadows & Friendly Pastels",
                List.of("Approachability", "Warmth", "Delight", "Psychological Safety"),
                "Educational tools, habit trackers, and wellness applications demand psychological safety and zero intimidation. Claymorphism’s soft, puffy 3D cards and rounded pill shapes reduce user anxiety, sparking curiosity and sustained daily engagement.",
                "Brutalism feels aggressive for young learners. Glassmorphism feels detached and sterile. Neo-Brutalism’s hard black borders create visual tension incompatible with calm mindfulness. Skeuomorphism clutters learning with heavy industrial textures.",
                tokens,
                tw,
                List.of(
                    "Soft squash-and-stretch on button click: transform: scale(0.96) with --dur-short (200ms) cubic-bezier(0.16, 1, 0.3, 1).",
                    "Hover lift: transform: translateY(-4px) with subtle expansion of drop shadow blur.",
                    "Stagger card entrances by 60ms with translateY(12px) spring deceleration."
                )
            );
        }

        // 3. Glassmorphism
        else if (containsAny(p, "health", "clinic", "patient", "medic", "doctor", "pharma", "legal", "contract", "compliance", "wealth", "invest", "executive", "luxury", "biotech")) {
            Map<String, String> tokens = new LinkedHashMap<>();
            tokens.put("--bg-canvas", "radial-gradient(ellipse at top, #0f172a 0%, #020617 100%)");
            tokens.put("--surface-glass", "rgba(255, 255, 255, 0.04)");
            tokens.put("--surface-glass-hover", "rgba(255, 255, 255, 0.08)");
            tokens.put("--border-hairline", "1px solid rgba(255, 255, 255, 0.14)");
            tokens.put("--backdrop-blur", "blur(16px) saturate(180%)");
            tokens.put("--shadow-elevation", "0 20px 40px -15px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.2)");
            tokens.put("--font-display", "'Inter', 'Geist Sans', system-ui, sans-serif");
            tokens.put("--accent-glow", "#38bdf8");
            tokens.put("--accent-emerald", "#10b981");

            Map<String, String> tw = new LinkedHashMap<>();
            tw.put("card", "bg-white/[0.04] backdrop-blur-md border border-white/[0.14] rounded-2xl shadow-[0_20px_40px_-15px_rgba(0,0,0,0.5),inset_0_1px_0_rgba(255,255,255,0.2)] p-6 text-slate-100");
            tw.put("button_primary", "bg-sky-500/80 hover:bg-sky-500 backdrop-blur-sm text-white font-medium px-5 py-2.5 rounded-xl border border-sky-400/40 shadow-[0_0_20px_rgba(56,189,248,0.3)] hover:scale-[1.02] active:scale-[0.98] transition-transform duration-150");
            tw.put("badge", "bg-white/[0.08] backdrop-blur-sm border border-white/20 text-sky-300 px-3 py-1 rounded-full text-xs font-semibold");
            tw.put("input", "bg-white/[0.03] backdrop-blur-sm border border-white/10 rounded-xl px-4 py-3 text-white placeholder-slate-400 focus:border-sky-400 focus:outline-none");

            return new FrontendAestheticDecision(
                "Glassmorphism (Frosted Precision Glass & Spatial Depth)",
                "Multi-Layered Translucent Glass, Specular Hairline Borders & Deep Frosted Blur",
                List.of("Clinical Trust", "High-End Authority", "Sophistication", "Clarity"),
                "High-stakes healthcare, legal governance, and executive analytics demand elite trust, authority, and immaculate clarity. Glassmorphism layers multi-tiered translucent glass sheets with frosted backdrop blurs and hairline specular borders, projecting next-generation technological superiority.",
                "Neo-Brutalism looks too rebellious and informal for hospital boards or legal compliance audits. Claymorphism looks like a preschool platform and compromises institutional credibility. Industrial Brutalism lacks executive elegance.",
                tokens,
                tw,
                List.of(
                    "Floating elevations: hover lifts card with translateY(-3px) and slight border opacity increase from 0.14 to 0.24.",
                    "Backdrop filter remains static to avoid expensive layout reflows during animations.",
                    "Animate only transform and opacity via cubic-bezier(0.16, 1, 0.3, 1)."
                )
            );
        }

        // 4. Neo-Brutalism
        else if (containsAny(p, "consumer", "b2c", "social", "creator", "influencer", "meme", "viral", "retail", "shop", "commerce", "fashion", "crypto", "web3", "nft", "gamers", "genz")) {
            Map<String, String> tokens = new LinkedHashMap<>();
            tokens.put("--bg-canvas", "#fef08a");
            tokens.put("--surface-card", "#ffffff");
            tokens.put("--border-thick", "3px solid #000000");
            tokens.put("--shadow-hard", "4px 4px 0px #000000");
            tokens.put("--shadow-hover", "6px 6px 0px #000000");
            tokens.put("--shadow-active", "1px 1px 0px #000000");
            tokens.put("--radius-neo", "8px");
            tokens.put("--font-display", "'Space Grotesk', 'Cabinet Grotesk', 'Archivo Black', sans-serif");
            tokens.put("--accent-pop-yellow", "#facc15");
            tokens.put("--accent-pop-pink", "#f43f5e");
            tokens.put("--accent-pop-cyan", "#06b6d4");

            Map<String, String> tw = new LinkedHashMap<>();
            tw.put("card", "bg-white border-[3px] border-black rounded-lg shadow-[4px_4px_0px_#000000] p-6 text-black");
            tw.put("button_primary", "bg-[#facc15] text-black font-extrabold border-[3px] border-black rounded-lg px-6 py-3 shadow-[4px_4px_0px_#000000] hover:shadow-[6px_6px_0px_#000000] hover:-translate-x-[2px] hover:-translate-y-[2px] active:shadow-[1px_1px_0px_#000000] active:translate-x-[3px] active:translate-y-[3px] transition-all duration-100");
            tw.put("badge", "bg-[#f43f5e] text-white font-black border-2 border-black px-3 py-1 rounded shadow-[2px_2px_0px_#000000] uppercase text-xs");
            tw.put("input", "bg-white border-[3px] border-black rounded-lg p-3 font-medium text-black focus:outline-none focus:bg-yellow-50");

            return new FrontendAestheticDecision(
                "Neo-Brutalism (High-Contrast Bold Pop & Kinetic Playfulness)",
                "Heavy Black Borders, Hard Offset Shadows (No Blur), Saturated Pop Accents & Unapologetic Typography",
                List.of("Irreverence", "High Energy", "Unforgettable Impact", "Playful Confidence"),
                "In crowded hackathon demo tracks, 90% of teams present identical muted dark-mode templates. For consumer, creator, and viral Web3 products, Neo-Brutalism cuts through instantly with high-voltage saturated palettes, bold black 3px borders, and hard zero-blur offset drop shadows that judges remember.",
                "Glassmorphism blends into corporate invisibility on a projector screen. Claymorphism is too soft and lacks bold punchy attitude. Industrial Brutalism feels like a server rack rather than an exciting consumer product.",
                tokens,
                tw,
                List.of(
                    "Zero-lag instantaneous button clicks: translate(3px, 3px) with shadow collapse from 4px to 1px.",
                    "Hover lift: translate(-2px, -2px) with shadow expanding to 6px 6px 0px #000.",
                    "Snap transitions strictly under --dur-micro (120ms) using snappy cubic-bezier(0.16, 1, 0.3, 1)."
                )
            );
        }

        // 5. Industrial Brutalism (Default / Mission-Critical)
        else {
            Map<String, String> tokens = new LinkedHashMap<>();
            tokens.put("--bg-canvas", "#070a0f");
            tokens.put("--surface-terminal", "#0d131f");
            tokens.put("--border-chassis", "1px solid #1c2738");
            tokens.put("--border-accent", "1px solid #00f59b");
            tokens.put("--shadow-raw", "none");
            tokens.put("--radius-zero", "2px");
            tokens.put("--font-mono", "'JetBrains Mono', 'Geist Mono', monospace");
            tokens.put("--font-display", "'Geist Sans', 'Inter', sans-serif");
            tokens.put("--accent-phosphor-green", "#00f59b");
            tokens.put("--accent-telemetry-cyan", "#00b4d8");
            tokens.put("--status-alert-red", "#ef4444");

            Map<String, String> tw = new LinkedHashMap<>();
            tw.put("card", "bg-[#0d131f] border border-[#1c2738] rounded-sm p-5 text-slate-200 font-mono");
            tw.put("button_primary", "bg-[#00f59b] text-[#070a0f] font-bold px-4 py-2 rounded-sm hover:bg-[#00d685] active:translate-y-[1px] transition-transform duration-100 uppercase tracking-wider text-xs");
            tw.put("badge", "border border-[#00f59b]/40 bg-[#00f59b]/10 text-[#00f59b] px-2.5 py-0.5 rounded-sm text-xs font-mono tracking-widest uppercase");
            tw.put("terminal_log", "bg-[#05070a] border border-[#141b27] rounded-sm p-4 font-mono text-xs text-emerald-400 overflow-x-auto");

            return new FrontendAestheticDecision(
                "Industrial Brutalism (Mission-Critical System Terminal HUD)",
                "High-Density Monospace Grid, Obsidian Surfaces, Zero-Decoration Wireframes & Telemetry Status LEDs",
                List.of("Technical Rigor", "Engineering Dominance", "Mathematical Certainty", "Mission-Critical Stability"),
                "For autonomous AI agents, cloud architectures, real-time telemetry, cybersecurity, and enterprise systems, Industrial Brutalism signals uncompromising engineering mastery. It strips away all frivolous AI-slop decorations in favor of high information density, stark monospace typography, real-time terminal streaming logs, and precision telemetry indicators.",
                "Neo-Brutalism and Claymorphism look frivolous and unserious for mission-critical infrastructure. Glassmorphism degrades text contrast and slows down terminal log rendering. Skeuomorphism consumes precious screen real estate.",
                tokens,
                tw,
                List.of(
                    "Animate only transform and opacity.",
                    "Micro-duration --dur-micro (100ms) for decisive state changes.",
                    "Live terminal text appends without layout shift using pre-allocated min-height containers.",
                    "Telemetry gauges update with GPU-composited transform: scaleX() and cubic-bezier(0.16, 1, 0.3, 1)."
                )
            );
        }
    }

    public Map<String, SquadMemberPrompt> generateSquadPrompts(String problem, String domain, SoftwarePatternDecision pattern, FrontendAestheticDecision aesthetic) {
        Map<String, SquadMemberPrompt> map = new LinkedHashMap<>();

        // Role 1: Backend Lead
        map.put("Backend Lead", new SquadMemberPrompt(
            "Backend API, Data Pipeline & Resilience Lead",
            "backend/",
            List.of("backend/src/app/main.py", "backend/src/app/api/v1/", "backend/src/app/core/redis.py", "backend/src/app/core/resilience.py"),
            List.of("fastapi-production-archetype", "async-agent-celery-redis", "llm-gateway-semantic-cache"),
            String.format(
                "You are the Backend API & Resilience Lead for our project: '%s' (%s).\n"
                + "Software Architecture Pattern: %s.\n"
                + "Your Responsibilities:\n"
                + "1. Implement async FastAPI endpoints wrapped in standardized ResponseEnvelope schemas.\n"
                + "2. Enforce Circuit Breakers (fail_max=3, reset_timeout=30s) on all external AI providers.\n"
                + "3. Integrate Redis semantic cache (<10ms) to bypass redundant LLM calls.\n"
                + "4. Run 'ruff check --fix . && pytest' before any git commit.",
                problem, domain, pattern.patternName()
            )
        ));

        // Role 2: Frontend Lead
        map.put("Frontend Lead", new SquadMemberPrompt(
            "Frontend UI, Design System & Real-Time Interaction Lead",
            "frontend/",
            List.of("frontend/index.html", "frontend/app.js", "frontend/style.css", "frontend/orbit-widget.js"),
            List.of("hallmark", "emil-design-eng", "minimalist-ui"),
            String.format(
                "You are the Frontend UI Lead for our project: '%s' (%s).\n"
                + "Frontend Aesthetic Paradigm: %s (%s).\n"
                + "Your Responsibilities:\n"
                + "1. Style all cards, inputs, and controls according to the '%s' design tokens.\n"
                + "2. Apply Emil Kowalski motion rules: animate only transform and opacity with cubic-bezier(0.16, 1, 0.3, 1).\n"
                + "3. Connect to backend Server-Sent Events (/api/v1/agent/query) for zero-latency token streaming.\n"
                + "4. Never display generic loading spinners; display informative execution steps.",
                problem, domain, aesthetic.aestheticName(), aesthetic.visualArchetype(), aesthetic.aestheticName()
            )
        ));

        // Role 3: AI / Agentic Lead
        map.put("AI Lead", new SquadMemberPrompt(
            "AI / Multi-Agent Systems & Vector Search Lead",
            "ai_layer/",
            List.of("ai_layer/langgraph_supervisor.py", "ai_layer/fastmcp_server.py", "ai_layer/eval_harness.py"),
            List.of("langgraph-production-patterns", "fastmcp-tool-server", "rag-reranking-pipeline", "agent-eval-harness"),
            String.format(
                "You are the AI / Multi-Agent Systems Lead for our project: '%s' (%s).\n"
                + "Architecture: %s.\n"
                + "Your Responsibilities:\n"
                + "1. Build the LangGraph StateGraph with a mandatory Human-in-the-Loop review gate.\n"
                + "2. Expose FastMCP isolated tools over Server-Sent Events (port 8001).\n"
                + "3. Enforce FlashRank reranking (top_k=5) over PostgreSQL pgvector hybrid search.\n"
                + "4. Maintain RAGAS faithfulness score >= 0.90 across 25 golden evaluation test cases.",
                problem, domain, pattern.patternName()
            )
        ));

        // Role 4: Database Lead
        map.put("Database Lead", new SquadMemberPrompt(
            "Database Schema, pgvector & Supabase RLS Lead",
            "database/",
            List.of("database/supabase_rls.sql", "database/schema.sql", "backend/src/app/models/document.py"),
            List.of("pgvector-hybrid-search", "agent-security-guardrails"),
            String.format(
                "You are the Database & Security Lead for our project: '%s' (%s).\n"
                + "Your Responsibilities:\n"
                + "1. Create PostgreSQL 16 schema with pgvector (dim=1536) and HNSW cosine index.\n"
                + "2. Implement Hybrid Search combining HNSW vector distance and tsvector BM25 using Reciprocal Rank Fusion (RRF).\n"
                + "3. Enforce Supabase Row-Level Security (RLS) on all multi-tenant tables.\n"
                + "4. Seed realistic domain data with 'python database/seed_data.py'.",
                problem, domain
            )
        ));

        // Role 5: DevOps / Pitch Lead
        map.put("DevOps Lead", new SquadMemberPrompt(
            "Cloud DevOps, CI/CD, Pitch Deck & Live Demo Lead",
            "infra/ and pitch/",
            List.of("infra/Dockerfile", "infra/docker-compose.yml", "pitch/pitch.marp.md", "pitch/demo.sh"),
            List.of("agent-docker-aws-deploy", "marp-presentation-engine", "archify"),
            String.format(
                "You are the Cloud DevOps & Pitch Lead for our project: '%s' (%s).\n"
                + "Your Responsibilities:\n"
                + "1. Validate multi-stage Docker build (<180MB non-root appuser) and AWS ECS Fargate task.\n"
                + "2. Author winning Marp pitch slides in 'pitch/pitch.marp.md' showcasing Archify blueprints.\n"
                + "3. Rehearse live terminal fail-safe script 'bash pitch/demo.sh' in case stage Wi-Fi drops.\n"
                + "4. Run 'npm run pitch' to compile standalone presentation HTML and PDF.",
                problem, domain
            )
        ));

        return map;
    }

    public SeniorGuidance getSeniorGuidance(String role, String branch, String knowledgeLevel) {
        String r = role.toLowerCase();
        String b = (branch != null && !branch.isBlank()) ? branch : "feat/core";

        if (r.contains("backend") || r.contains("api")) {
            return new SeniorGuidance(
                "Backend API, Data Pipeline & Resilience Lead",
                b,
                "Ship async streaming routes, enforce circuit breakers, and connect Redis semantic caching.",
                List.of(
                    "Implement FastAPI route in 'backend/src/app/api/v1/' using ResponseEnvelope.",
                    "Wrap external LLM calls with circuit_breaker(failure_threshold=3, recovery_timeout=30.0).",
                    "Add Redis semantic caching to achieve sub-10ms query responses.",
                    "Verify automated tests by running 'PYTHONPATH=backend pytest backend/tests/'."
                ),
                List.of(
                    "NEVER write blocking synchronous time.sleep() or requests.get() inside async def routes.",
                    "NEVER return raw unvalidated JSON dictionaries without Pydantic schema validation.",
                    "NEVER bypass Circuit Breaker protection on third-party APIs.",
                    "NEVER hardcode database URLs or API keys in source code."
                ),
                List.of(
                    "Check that all routes use dependency injection (Depends(get_db)).",
                    "Ensure every endpoint handles HTTPException gracefully.",
                    "Verify p95 response time remains below 300ms."
                ),
                List.of("backend/src/app/main.py", "backend/src/app/api/v1/", "backend/src/app/core/redis.py", "backend/src/app/core/resilience.py"),
                List.of("Sync calls in async event loop", "Missing DTO response models", "Unprotected external API calls"),
                "Judges test concurrency. If two judges hit your demo endpoint at once, single-threaded sync code freezes. Async + Redis keeps it blistering fast."
            );
        } else if (r.contains("database") || r.contains("data") || r.contains("vector")) {
            return new SeniorGuidance(
                "Database, pgvector & Supabase RLS Lead",
                b,
                "Configure PostgreSQL 16, pgvector HNSW indexing, and multi-tenant Row-Level Security.",
                List.of(
                    "Create HNSW vector index: 'CREATE INDEX ON docs USING hnsw (embedding vector_cosine_ops)'.",
                    "Implement Hybrid Search (pgvector Cosine <=> + tsvector BM25) with Reciprocal Rank Fusion.",
                    "Apply Supabase Row-Level Security policies in 'database/supabase_rls.sql'.",
                    "Seed 50+ realistic domain documents using 'python database/seed_data.py'."
                ),
                List.of(
                    "NEVER concatenate user input into raw SQL queries; use SQLAlchemy parameterized queries.",
                    "NEVER run sequential scans without vector indexes on tables with >1,000 embeddings.",
                    "NEVER disable Row-Level Security (RLS) on multi-tenant production tables."
                ),
                List.of(
                    "Verify EXPLAIN ANALYZE shows Index Scan using HNSW index.",
                    "Check that RLS policies prevent cross-tenant data leakage.",
                    "Confirm vector dimensions match model output exactly (1536)."
                ),
                List.of("database/supabase_rls.sql", "database/seed_data.py", "backend/src/app/models/document.py"),
                List.of("SQL injection vulnerability", "Missing HNSW index", "Cross-tenant data leakage"),
                "Show the judges 'EXPLAIN ANALYZE' during the pitch. An HNSW Index Scan proves you built a production database, not a toy."
            );
        } else if (r.contains("ai") || r.contains("agent") || r.contains("langgraph")) {
            return new SeniorGuidance(
                "AI / Multi-Agent Systems & Vector Search Lead",
                b,
                "Architect LangGraph supervisor, human-in-the-loop review gate, and FastMCP tools.",
                List.of(
                    "Construct LangGraph StateGraph in 'ai_layer/langgraph_supervisor.py'.",
                    "Implement interrupt_before=['human_approval'] gate before irreversible actions.",
                    "Expose tool functions via FastMCP Server-Sent Events on port 8001.",
                    "Benchmark RAGAS faithfulness >= 0.90 using 'python ai_layer/eval_harness.py'."
                ),
                List.of(
                    "NEVER allow an autonomous agent to execute database writes without human approval.",
                    "NEVER loop agent reasoning indefinitely; enforce max_iterations=5.",
                    "NEVER deploy without measuring RAGAS faithfulness metrics."
                ),
                List.of(
                    "Verify LangGraph state transitions handle error edges gracefully.",
                    "Ensure FastMCP tool parameters have strict JSON Schema validation.",
                    "Check that RAGAS evaluation scores are saved in 'pitch/eval_results.json'."
                ),
                List.of("ai_layer/langgraph_supervisor.py", "ai_layer/fastmcp_server.py", "ai_layer/eval_harness.py"),
                List.of("Infinite agent loops", "Autonomous unchecked writes", "Unmeasured hallucinations"),
                "When you demonstrate the Human-in-the-Loop approval gate live, enterprise judges will nod in approval. It proves enterprise safety."
            );
        } else if (r.contains("front") || r.contains("ui") || r.contains("web")) {
            return new SeniorGuidance(
                "Frontend UI, Design System & Real-Time Interaction Lead",
                b,
                "Build real-time terminal streaming UI, apply Emil Kowalski motion tokens, and eliminate layout shifts.",
                List.of(
                    "Connect EventSource listener to backend SSE endpoint for real-time token streaming.",
                    "Implement chosen design tokens from 'FrontendAestheticDecision'.",
                    "Use Emil Kowalski motion tokens: cubic-bezier(0.16, 1, 0.3, 1), animate only transform and opacity.",
                    "Add interactive Archify architecture modal for pitch demonstration."
                ),
                List.of(
                    "NEVER show a blank screen or static spinner during 10-second agent reasoning.",
                    "NEVER animate layout properties like width, height, margin, or padding; use transform.",
                    "NEVER commit unhandled Promise rejections that freeze the browser console."
                ),
                List.of(
                    "Verify UI responsiveness on both mobile and 4K stage projector resolutions.",
                    "Ensure contrast ratios pass WCAG AA accessibility standards.",
                    "Confirm token streaming renders smoothly without flickering."
                ),
                List.of("frontend/index.html", "frontend/app.js", "frontend/style.css", "frontend/orbit-widget.js"),
                List.of("Static spinners without feedback", "Layout thrashing during streaming", "Broken high-resolution scaling"),
                "Live token streaming mesmerizes judges. While competitors make them stare at a spinner, your UI streams every reasoning step in real-time."
            );
        } else {
            return new SeniorGuidance(
                "Cloud DevOps, CI/CD, Pitch Deck & Live Demo Lead",
                b,
                "Build minimal non-root Docker container (<180MB), compile Marp slides, and rehearse stage fail-safe.",
                List.of(
                    "Verify 'infra/Dockerfile' compiles minimal image running as non-root appuser.",
                    "Test AWS ECS Fargate task definition and ALB health check on '/api/v1/health'.",
                    "Compile 'pitch/pitch.marp.md' into interactive HTML and standalone PDF via 'node bin/cli.js pitch'.",
                    "Rehearse stage fail-safe runner 'bash pitch/demo.sh' for 100% offline backup."
                ),
                List.of(
                    "NEVER run production Docker containers as the root user.",
                    "NEVER commit secrets, private keys, or .env files to git.",
                    "NEVER wait until Hour 23 to write your pitch deck; draft slides at Hour 6.",
                    "NEVER rely on venue Wi-Fi on stage without an offline terminal fail-safe."
                ),
                List.of(
                    "Verify Docker image size is under 180MB.",
                    "Check that health check responds with HTTP 200 in under 100ms.",
                    "Ensure Marp presentation renders crisp high-DPI typography."
                ),
                List.of("infra/Dockerfile", "pitch/pitch.marp.md", "pitch/demo.sh", "infra/docker-compose.yml"),
                List.of("Root containers in production", "Leaked API keys", "Unrehearsed stage presentation"),
                "Run 'bash pitch/demo.sh' in a background terminal before going on stage. If Wi-Fi crashes, switch to that terminal and win the hackathon."
            );
        }
    }

    public String generateArchitecturalEssay(String problem, String domain, SoftwarePatternDecision pattern, FrontendAestheticDecision aesthetic) {
        StringBuilder sb = new StringBuilder();
        sb.append(String.format("### 🏛️ Deep Architectural Rationale & Why This Guarantees Hackathon Victory\n\n"));
        sb.append(String.format("**Problem Statement**: %s\n", problem));
        sb.append(String.format("**Domain Classification**: %s\n", domain));
        sb.append(String.format("**Selected Software Design Pattern**: %s\n", pattern.patternName()));
        sb.append(String.format("**Selected Frontend Aesthetic Paradigm**: %s\n\n", aesthetic.aestheticName()));

        sb.append("#### 1. The 24-Hour Velocity & Reliability Equation\n");
        sb.append("In high-stakes hackathons, 80% of teams fail not because of weak ideas, but because of architectural overengineering. ");
        sb.append("Teams that choose microservices inevitably spend 14 hours debugging cross-container CORS headers, Docker network bridges, ");
        sb.append("and uncoordinated database migrations, presenting a half-broken prototype on stage. Conversely, teams that build naive single-file ");
        sb.append("scripts freeze when judges test concurrent requests or when LLM API calls take 12 seconds.\n\n");
        sb.append(String.format("Orbit has selected the **%s** pattern because it solves this dilemma definitively: %s\n\n", pattern.patternName(), pattern.whyChosen()));

        sb.append("#### 2. Why Microservices Were Rejected for This Mission\n");
        sb.append(pattern.whyNotMicroservices()).append("\n\n");

        sb.append("#### 3. Why the Naive Monolith Was Rejected\n");
        sb.append(pattern.whyNotSimpleMonolith()).append("\n\n");

        sb.append("#### 4. Frontend Visual Strategy: Why ").append(aesthetic.aestheticName()).append(" Dominates\n");
        sb.append(aesthetic.whyPerfectFit()).append("\n");
        sb.append("When evaluating competing hackathon projects, judges spend an average of 90 seconds looking at the user interface. ");
        sb.append(aesthetic.whyNotAlternatives()).append("\n\n");

        sb.append("#### 5. Defense-in-Depth Engineering: Resilience & Observability\n");
        sb.append("Unlike fragile hackathon prototypes, our architecture incorporates production-grade enterprise resilience:\n");
        sb.append("- **Sub-10ms Semantic Caching**: Powered by Redis, bypassing expensive LLM calls for repeated domain queries.\n");
        sb.append("- **Resilience Decorators**: Circuit breakers (fail_max=3, reset_timeout=30s) shield the application from upstream AI provider downtime.\n");
        sb.append("- **Mathematical Faithfulness**: FlashRank cross-encoder reranking combined with pgvector HNSW hybrid search guarantees RAGAS faithfulness >= 0.90.\n");
        sb.append("- **Human-in-the-Loop Safety Gate**: Critical write actions are paused in LangGraph until an authorized human approves them.\n\n");

        return sb.toString();
    }

    public String generateFullReport(String problem) {
        String domain = inferDomain(problem);
        SoftwarePatternDecision pattern = decideSoftwarePattern(problem);
        FrontendAestheticDecision aesthetic = decideFrontendAesthetic(problem);
        Map<String, SquadMemberPrompt> prompts = generateSquadPrompts(problem, domain, pattern, aesthetic);
        String essay = generateArchitecturalEssay(problem, domain, pattern, aesthetic);

        StringBuilder sb = new StringBuilder();
        sb.append("# 🤖 Orbit Senior Principal Mascot Director Report\n\n");
        sb.append("> **Autonomous Decision Engine**: ").append(MASCOT_NAME).append(" | **Engine**: Java OpenJDK 17 Enterprise Edition\n\n");
        sb.append("## 🎯 Problem Statement Analysis\n");
        sb.append("* **Input Statement**: `").append(problem).append("`\n");
        sb.append("* **Domain Classified**: **").append(domain).append("**\n");
        sb.append("* **Recommended Architectural Pattern**: **").append(pattern.patternName()).append("**\n");
        sb.append("* **Recommended Frontend Aesthetic**: **").append(aesthetic.aestheticName()).append("**\n\n");

        sb.append(essay).append("\n");

        sb.append("## 🎨 Frontend Design Tokens (").append(aesthetic.aestheticName()).append(")\n\n");
        sb.append("```css\n:root {\n");
        for (Map.Entry<String, String> e : aesthetic.cssDesignTokens().entrySet()) {
            sb.append("  ").append(e.getKey()).append(": ").append(e.getValue()).append(";\n");
        }
        sb.append("}\n```\n\n");

        sb.append("### Motion & Interaction Rules:\n");
        for (String rule : aesthetic.motionInteractionRules()) {
            sb.append("* ").append(rule).append("\n");
        }
        sb.append("\n");

        sb.append("## 👥 Ready-Made Teammate Boilerplate Prompts\n");
        sb.append("Copy and paste these exact prompts directly into each teammate's Agentic IDE (Antigravity, Claude, Cursor, Hero):\n\n");

        for (Map.Entry<String, SquadMemberPrompt> e : prompts.entrySet()) {
            SquadMemberPrompt p = e.getValue();
            sb.append("### 👤 ").append(p.roleTitle()).append("\n");
            sb.append("* **Assigned Layer**: `").append(p.targetLayer()).append("`\n");
            sb.append("* **Core Files**: `").append(String.join("`, `", p.coreFiles())).append("`\n");
            sb.append("* **Pre-Installed Skills**: `").append(String.join("`, `", p.assignedSkills())).append("`\n\n");
            sb.append("```markdown\n").append(p.promptBody()).append("\n```\n\n");
        }

        sb.append("---\n*Generated autonomously by Java HSF Mascot Director for Sathvik's Hackathon Squad.* 🚀\n");
        return sb.toString();
    }

    public String generateJson(String problem) {
        String domain = inferDomain(problem);
        SoftwarePatternDecision pattern = decideSoftwarePattern(problem);
        FrontendAestheticDecision aesthetic = decideFrontendAesthetic(problem);
        Map<String, SquadMemberPrompt> prompts = generateSquadPrompts(problem, domain, pattern, aesthetic);

        StringBuilder json = new StringBuilder();
        json.append("{\n");
        json.append("  \"mascot\": \"").append(escapeJson(MASCOT_NAME)).append("\",\n");
        json.append("  \"engine\": \"Java OpenJDK 17\",\n");
        json.append("  \"problem_statement\": \"").append(escapeJson(problem)).append("\",\n");
        json.append("  \"domain\": \"").append(escapeJson(domain)).append("\",\n");
        json.append("  \"software_pattern\": {\n");
        json.append("    \"name\": \"").append(escapeJson(pattern.patternName())).append("\",\n");
        json.append("    \"style\": \"").append(escapeJson(pattern.architecturalStyle())).append("\",\n");
        json.append("    \"why_chosen\": \"").append(escapeJson(pattern.whyChosen())).append("\"\n");
        json.append("  },\n");
        json.append("  \"frontend_aesthetic\": {\n");
        json.append("    \"name\": \"").append(escapeJson(aesthetic.aestheticName())).append("\",\n");
        json.append("    \"archetype\": \"").append(escapeJson(aesthetic.visualArchetype())).append("\",\n");
        json.append("    \"why_perfect_fit\": \"").append(escapeJson(aesthetic.whyPerfectFit())).append("\"\n");
        json.append("  },\n");
        json.append("  \"teammates\": [\n");
        int count = 0;
        for (Map.Entry<String, SquadMemberPrompt> e : prompts.entrySet()) {
            SquadMemberPrompt p = e.getValue();
            json.append("    {\n");
            json.append("      \"role\": \"").append(escapeJson(p.roleTitle())).append("\",\n");
            json.append("      \"layer\": \"").append(escapeJson(p.targetLayer())).append("\"\n");
            json.append("    }").append(++count < prompts.size() ? "," : "").append("\n");
        }
        json.append("  ]\n");
        json.append("}\n");
        return json.toString();
    }

    private static boolean containsAny(String text, String... words) {
        for (String w : words) {
            if (text.contains(w)) return true;
        }
        return false;
    }

    private static String escapeJson(String raw) {
        if (raw == null) return "";
        return raw.replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", "\\n").replace("\r", "");
    }

    // --- CLI Entrypoint ---

    public static void main(String[] args) {
        HSFMascotDirector director = new HSFMascotDirector();

        if (args.length == 0) {
            String defaultProblem = "AI-Powered Autonomous Healthcare Diagnostics & Clinical RAG";
            System.out.println(director.generateFullReport(defaultProblem));
            return;
        }

        if (args[0].equals("--onboard") && args.length >= 5) {
            String name = args[1];
            String role = args[2];
            String branch = args[3];
            String goal = args[4];
            SeniorGuidance g = director.getSeniorGuidance(role, branch, "Intermediate");
            System.out.println(String.format("👋 Welcome %s! Senior Orbit is pairing on branch '%s'.", name, branch));
            System.out.println(String.format("Mission: %s", goal));
            System.out.println("Immediate Actions:");
            for (String a : g.immediateActions()) System.out.println(" - " + a);
            System.out.println("Guardrails:");
            for (String w : g.criticalGuardrails()) System.out.println(" - " + w);
            return;
        }

        String problem = args[0];
        boolean asJson = args.length > 1 && args[1].equalsIgnoreCase("--json");

        if (asJson) {
            System.out.println(director.generateJson(problem));
        } else {
            System.out.println(director.generateFullReport(problem));
        }
    }
}
