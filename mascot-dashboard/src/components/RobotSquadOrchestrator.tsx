'use client';

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Bot, 
  ShieldAlert, 
  Palette, 
  Cpu, 
  Database, 
  Rocket, 
  Users, 
  CheckCircle2, 
  ChevronRight,
  Layers,
  Sparkles,
  Flame
} from 'lucide-react';

interface Autobot {
  codename: string;
  callsign: string;
  avatar: string;
  targetLayer: string;
  motto: string;
  color: string;
  skills: string[];
  tasks: string[];
}

const AUTOBOTS: Autobot[] = [
  {
    codename: 'Orbit Prime 🤖👑',
    callsign: 'Supreme Commander & Master Architect',
    avatar: '🤖',
    targetLayer: 'Orchestration & Governance',
    motto: 'Autobots, roll out! Zero wasted minutes, zero technical debt.',
    color: 'from-amber-500/20 to-orange-600/20 border-amber-500/40 text-amber-400',
    skills: ['hackathon-speedrun-kit', 'jev-decision-router', 'hallmark'],
    tasks: ['Decomposes problem into modular specs', 'Enforces Hexagonal / Event-Driven architecture', 'Guards MVP submission deadline']
  },
  {
    codename: 'Ironhide 🛡️⚡',
    callsign: 'Backend Titan & Resilience Sentinel',
    avatar: '🛡️',
    targetLayer: 'Backend API & Middleware',
    motto: 'My circuits do not break. Throughput stays high, latency stays low.',
    color: 'from-red-500/20 to-rose-600/20 border-red-500/40 text-red-400',
    skills: ['fastapi-production-archetype', 'async-agent-celery-redis', 'llm-gateway-semantic-cache'],
    tasks: ['Async FastAPI routes with ResponseEnvelope[T]', 'Redis distributed SETNX mutex locks', 'Circuit breakers: 3 fails -> OPEN, 30s reset']
  },
  {
    codename: 'Mirage 🎨✨',
    callsign: 'Frontend Hologram Specialist',
    avatar: '🎨',
    targetLayer: 'Frontend & User Experience',
    motto: 'If the interface does not inspire in 3 seconds, the battle is already lost.',
    color: 'from-cyan-500/20 to-blue-600/20 border-cyan-500/40 text-cyan-400',
    skills: ['hallmark', 'context7-docs-fetcher'],
    tasks: ['Zero layout shift with Next.js 14 App Router', 'Emil Kowalski spring motion tokens', '5 dynamic visual aesthetics switcher']
  },
  {
    codename: 'Wheeljack 🔬⚡',
    callsign: 'AI & Multi-Agent Weaponsmith',
    avatar: '🔬',
    targetLayer: 'AI Layer & Multi-Agent',
    motto: 'Pure engineering brilliance! State graphs with deterministic execution.',
    color: 'from-emerald-500/20 to-teal-600/20 border-emerald-500/40 text-emerald-400',
    skills: ['langgraph-production-patterns', 'fastmcp-tool-server', 'rag-reranking-pipeline', 'agent-eval-harness'],
    tasks: ['Cyclic LangGraph supervisor state machines', 'FastMCP SSE tool server protocol', 'FlashRank TinyBERT reranker (<20ms)']
  },
  {
    codename: 'Ratchet 🏥💾',
    callsign: 'Database & Security Guardian',
    avatar: '💾',
    targetLayer: 'Database & Storage',
    motto: 'Data integrity is non-negotiable. Not a single byte compromised.',
    color: 'from-purple-500/20 to-indigo-600/20 border-purple-500/40 text-purple-400',
    skills: ['pgvector-hybrid-search', 'agent-security-guardrails'],
    tasks: ['PostgreSQL 16 schemas & ACID constraints', 'pgvector 1536-dim HNSW Cosine Index', 'Supabase Row-Level Security (RLS)']
  },
  {
    codename: 'Bumblebee 🐝🚀',
    callsign: 'Cloud DevOps & Stage Scout',
    avatar: '🚀',
    targetLayer: 'Cloud DevOps & Presentation',
    motto: 'Fast, nimble, reliable. The live demo will never crash on stage.',
    color: 'from-yellow-500/20 to-amber-600/20 border-yellow-500/40 text-yellow-400',
    skills: ['agent-docker-aws-deploy', 'poetry-python-packaging', 'marp-presentation-engine'],
    tasks: ['Multi-stage Docker builds (<180MB)', 'AWS ECS Fargate task definitions', 'Offline-resilient demo.sh stage fallback']
  }
];

export function RobotSquadOrchestrator() {
  const [teamSize, setTeamSize] = useState<number>(5);
  const [selectedLayer, setSelectedLayer] = useState<string>('frontend');
  const [activeBot, setActiveBot] = useState<Autobot>(AUTOBOTS[0]);

  const getArchetype = (size: number) => {
    switch (size) {
      case 1:
        return {
          title: 'Solo Pioneer',
          badge: '1 Engineer + 6 Autobot Co-Pilots',
          desc: 'Fullstack developer executes vertical slices from pgvector to UI with automated AI guardrails.'
        };
      case 2:
        return {
          title: 'Dynamic Duo',
          badge: 'Product & UX Lead + AI & Data Architect',
          desc: 'Lead 1 drives user experience and frontend/API; Lead 2 drives LangGraph, vector search, and cloud.'
        };
      case 3:
        return {
          title: 'Trio Strike Team',
          badge: 'Frontend Lead + Backend Lead + AI & Data Lead',
          desc: 'Specialized 3-prong attack separating UI, resilient API middleware, and cognitive intelligence.'
        };
      case 4:
        return {
          title: 'Core Four',
          badge: 'Frontend + Backend + AI + Data/DevOps',
          desc: 'High velocity quad covering all primary development pillars in parallel branches.'
        };
      case 5:
        return {
          title: 'Full Pentad',
          badge: 'Standard 5-Lead Division',
          desc: 'Complete Autobot pairing: dedicated Frontend, Backend, AI, Database, and Cloud/Pitch leads.'
        };
      default:
        return {
          title: `Extended League (${size} Members)`,
          badge: 'Pentad + Dedicated QA / Evaluation / Storyteller Pods',
          desc: 'Autonomous pod scaling: 5 core leads plus dedicated RAGAS evaluation, load testing, and pitch rehearsal.'
        };
    }
  };

  const archetype = getArchetype(teamSize);

  return (
    <div className="bg-[#0b0f17] border border-[#1e293b] rounded-2xl p-6 lg:p-8 shadow-2xl space-y-8">
      {/* Header */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-[#1e293b] pb-6">
        <div>
          <div className="flex items-center gap-2 text-amber-400 font-mono text-xs uppercase tracking-widest mb-1">
            <Flame className="w-4 h-4 text-orange-500 animate-pulse" />
            Transformers Autonomous Robot Squad
          </div>
          <h2 className="text-2xl lg:text-3xl font-extrabold text-white tracking-tight flex items-center gap-2">
            Autobot Companion Fleet & Variable Team Orchestrator
          </h2>
          <p className="text-sm text-slate-400 mt-1">
            Autonomous multi-agent squad dynamically re-partitioning responsibilities across all technical layers.
          </p>
        </div>

        {/* Team Size Slider */}
        <div className="bg-[#131b2a] border border-[#24334a] rounded-xl p-3 px-5 flex items-center gap-4">
          <div className="flex items-center gap-2">
            <Users className="w-4 h-4 text-cyan-400" />
            <span className="text-xs font-mono text-slate-300">Team Size:</span>
            <span className="text-lg font-bold text-cyan-400 font-mono">{teamSize}</span>
          </div>
          <input
            type="range"
            min="1"
            max="6"
            value={teamSize}
            onChange={(e) => setTeamSize(parseInt(e.target.value))}
            className="w-32 accent-cyan-400 cursor-pointer"
          />
        </div>
      </div>

      {/* Team Strategy Archetype Banner */}
      <div className="bg-gradient-to-r from-blue-950/40 via-cyan-950/30 to-purple-950/40 border border-cyan-800/40 rounded-xl p-4 flex flex-col md:flex-row items-start md:items-center justify-between gap-3">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-sm font-bold text-white uppercase tracking-wider">{archetype.title}</span>
            <span className="text-xs bg-cyan-900/60 text-cyan-300 px-2.5 py-0.5 rounded-full border border-cyan-700/50 font-mono">
              {archetype.badge}
            </span>
          </div>
          <p className="text-xs text-slate-300 mt-1">{archetype.desc}</p>
        </div>
        <div className="text-xs font-mono text-emerald-400 flex items-center gap-1.5 self-end md:self-center">
          <CheckCircle2 className="w-4 h-4" />
          <span>Synchronized with .hsf/traces.jsonl</span>
        </div>
      </div>

      {/* Autobots Grid */}
      <div>
        <h3 className="text-xs font-mono uppercase text-slate-400 tracking-wider mb-4 flex items-center gap-2">
          <Bot className="w-4 h-4 text-amber-400" />
          The 6 Specialized Autobot Companions
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {AUTOBOTS.map((bot) => (
            <motion.div
              key={bot.codename}
              whileHover={{ scale: 1.02 }}
              onClick={() => setActiveBot(bot)}
              className={`p-4 rounded-xl border cursor-pointer transition-all ${
                activeBot.codename === bot.codename
                  ? 'bg-[#151f30] border-cyan-400 shadow-lg shadow-cyan-950/50'
                  : 'bg-[#101725] border-[#1e293b] hover:border-slate-600'
              }`}
            >
              <div className="flex items-start justify-between">
                <div>
                  <h4 className="text-base font-bold text-white flex items-center gap-1.5">
                    {bot.codename}
                  </h4>
                  <p className="text-xs text-slate-400 mt-0.5">{bot.callsign}</p>
                </div>
                <span className="text-xs px-2 py-0.5 rounded bg-[#1c273c] text-cyan-300 font-mono border border-slate-700">
                  {bot.targetLayer.split('&')[0]}
                </span>
              </div>
              <p className="text-xs italic text-slate-300 mt-3 font-serif border-l-2 border-slate-700 pl-2">
                "{bot.motto}"
              </p>
              <div className="flex flex-wrap gap-1 mt-3">
                {bot.skills.slice(0, 2).map((sk) => (
                  <span key={sk} className="text-[10px] bg-slate-800 text-slate-300 px-1.5 py-0.5 rounded font-mono">
                    {sk}
                  </span>
                ))}
                {bot.skills.length > 2 && (
                  <span className="text-[10px] bg-slate-800 text-slate-400 px-1 py-0.5 rounded font-mono">
                    +{bot.skills.length - 2}
                  </span>
                )}
              </div>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Selected Autobot Deep Dive */}
      <div className="bg-[#101725] border border-cyan-900/50 rounded-xl p-5">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-3 border-b border-slate-800 pb-3">
          <div className="flex items-center gap-3">
            <span className="text-3xl">{activeBot.avatar}</span>
            <div>
              <h4 className="text-lg font-bold text-white">{activeBot.codename} &bull; {activeBot.callsign}</h4>
              <p className="text-xs text-cyan-400 font-mono">Target Technical Layer: {activeBot.targetLayer}</p>
            </div>
          </div>
          <span className="text-xs text-slate-400 italic">Autobot Companion Active</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
          <div>
            <h5 className="text-xs font-mono uppercase text-slate-400 mb-2">Core Tactical Responsibilities:</h5>
            <ul className="space-y-1.5 text-xs text-slate-300">
              {activeBot.tasks.map((task, i) => (
                <li key={i} className="flex items-start gap-2">
                  <ChevronRight className="w-3.5 h-3.5 text-cyan-400 shrink-0 mt-0.5" />
                  <span>{task}</span>
                </li>
              ))}
            </ul>
          </div>
          <div>
            <h5 className="text-xs font-mono uppercase text-slate-400 mb-2">Assigned Repository Skills:</h5>
            <div className="flex flex-wrap gap-1.5">
              {activeBot.skills.map((skill) => (
                <span
                  key={skill}
                  className="text-xs bg-cyan-950/80 text-cyan-300 border border-cyan-800/60 px-2.5 py-1 rounded-md font-mono"
                >
                  {skill}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Universal 5-Layer Features Menu */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-xs font-mono uppercase text-slate-400 tracking-wider flex items-center gap-2">
            <Layers className="w-4 h-4 text-purple-400" />
            Universal 5-Layer System Features Menu
          </h3>
          <span className="text-xs text-slate-500 font-mono">Production Pre-Ready</span>
        </div>

        {/* Layer Tabs */}
        <div className="flex flex-wrap gap-2 border-b border-slate-800 pb-2">
          {[
            { id: 'frontend', label: '🎨 Frontend Menu (Mirage)' },
            { id: 'backend', label: '🛡️ Backend Menu (Ironhide)' },
            { id: 'database', label: '💾 Database Menu (Ratchet)' },
            { id: 'ai', label: '🔬 AI Multi-Agent Menu (Wheeljack)' },
            { id: 'devops', label: '🚀 DevOps & Cloud Menu (Bumblebee)' }
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setSelectedLayer(tab.id)}
              className={`px-3 py-1.5 rounded-lg text-xs font-mono transition-all ${
                selectedLayer === tab.id
                  ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/50 shadow-sm'
                  : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Tab Content */}
        <div className="bg-[#121927] border border-slate-800 rounded-xl p-5">
          {selectedLayer === 'frontend' && (
            <div className="space-y-3">
              <h4 className="text-sm font-bold text-white">Frontend UI & Visual Experience (Mirage)</h4>
              <p className="text-xs text-slate-300">
                Next.js 14 App Router with Tailwind CSS, Framer Motion, and 5 dynamic aesthetic paradigms.
              </p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                <div className="bg-slate-900/60 p-3 rounded-lg border border-slate-800">
                  <div className="font-bold text-cyan-400">Live Mission Control Dashboard</div>
                  <div className="text-slate-400 mt-1">High-density telemetry feed, real-time widgets, responsive tables.</div>
                </div>
                <div className="bg-slate-900/60 p-3 rounded-lg border border-slate-800">
                  <div className="font-bold text-cyan-400">SSE Progress Token Streamer</div>
                  <div className="text-slate-400 mt-1">Direct token channel rendering LLM outputs with zero layout shift.</div>
                </div>
                <div className="bg-slate-900/60 p-3 rounded-lg border border-slate-800">
                  <div className="font-bold text-cyan-400">Human-in-the-Loop Modal</div>
                  <div className="text-slate-400 mt-1">Accessible modal dialog intercepting irreversible agent write actions.</div>
                </div>
                <div className="bg-slate-900/60 p-3 rounded-lg border border-slate-800">
                  <div className="font-bold text-cyan-400">5-Aesthetic Style Engine</div>
                  <div className="text-slate-400 mt-1">Skeuomorphism, Claymorphism, Glassmorphism, Neo & Industrial Brutalism.</div>
                </div>
              </div>
            </div>
          )}

          {selectedLayer === 'backend' && (
            <div className="space-y-3">
              <h4 className="text-sm font-bold text-white">Backend API & Resilience Sentinel (Ironhide)</h4>
              <p className="text-xs text-slate-300">
                FastAPI 0.115+ async microservice with ResponseEnvelope[T], Redis distributed mutex locks, and circuit breakers.
              </p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                <div className="bg-slate-900/60 p-3 rounded-lg border border-slate-800">
                  <div className="font-bold text-red-400">Chunked Ingestion Pipeline</div>
                  <div className="text-slate-400 mt-1">POST /api/v1/:domain/ingest with SHA-256 deduplication and async worker dispatch.</div>
                </div>
                <div className="bg-slate-900/60 p-3 rounded-lg border border-slate-800">
                  <div className="font-bold text-red-400">Hybrid RRF Query Search</div>
                  <div className="text-slate-400 mt-1">POST /api/v1/:domain/query fusing dense vector search and sparse BM25 text rank.</div>
                </div>
                <div className="bg-slate-900/60 p-3 rounded-lg border border-slate-800">
                  <div className="font-bold text-red-400">Distributed Idempotency Locks</div>
                  <div className="text-slate-400 mt-1">Redis SETNX lock:idempotency:&lt;key&gt; preventing double-execution on network retries.</div>
                </div>
                <div className="bg-slate-900/60 p-3 rounded-lg border border-slate-800">
                  <div className="font-bold text-red-400">Circuit Breaker Telemetry</div>
                  <div className="text-slate-400 mt-1">Fail-safe state monitoring (CLOSED, OPEN, HALF_OPEN) shielding from external AI outage.</div>
                </div>
              </div>
            </div>
          )}

          {selectedLayer === 'database' && (
            <div className="space-y-3">
              <h4 className="text-sm font-bold text-white">Database & Vector Storage (Ratchet)</h4>
              <p className="text-xs text-slate-300">
                PostgreSQL 16 relational engine with pgvector, HNSW index, GIN BM25 tsvector, and Supabase Row-Level Security.
              </p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                <div className="bg-slate-900/60 p-3 rounded-lg border border-slate-800">
                  <div className="font-bold text-purple-400">HNSW Cosine Vector Index</div>
                  <div className="text-slate-400 mt-1">1536-dimensional embeddings indexed via HNSW (m=16, ef_construction=64) in sub-12ms.</div>
                </div>
                <div className="bg-slate-900/60 p-3 rounded-lg border border-slate-800">
                  <div className="font-bold text-purple-400">Supabase Row-Level Security</div>
                  <div className="text-slate-400 mt-1">Tenant isolation policies ensuring judge multi-tenant security verification.</div>
                </div>
                <div className="bg-slate-900/60 p-3 rounded-lg border border-slate-800">
                  <div className="font-bold text-purple-400">Immutable Audit Trail Log</div>
                  <div className="text-slate-400 mt-1">Tamper-evident log of all user operations and agentic decisions for judges.</div>
                </div>
                <div className="bg-slate-900/60 p-3 rounded-lg border border-slate-800">
                  <div className="font-bold text-purple-400">SQLAlchemy 2.0 AsyncEngine</div>
                  <div className="text-slate-400 mt-1">Non-blocking connection pool with pre-ping validation and SSL encryption.</div>
                </div>
              </div>
            </div>
          )}

          {selectedLayer === 'ai' && (
            <div className="space-y-3">
              <h4 className="text-sm font-bold text-white">AI & Multi-Agent Cognitive Weaponsmith (Wheeljack)</h4>
              <p className="text-xs text-slate-300">
                LangGraph cyclic state machines, FastMCP tools protocol over SSE, and FlashRank neural reranking.
              </p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                <div className="bg-slate-900/60 p-3 rounded-lg border border-emerald-400/40">
                  <div className="font-bold text-emerald-400">Cyclic LangGraph Supervisor</div>
                  <div className="text-slate-400 mt-1">Deterministic state machine coordinating specialists with recursion_limit=5.</div>
                </div>
                <div className="bg-slate-900/60 p-3 rounded-lg border border-emerald-400/40">
                  <div className="font-bold text-emerald-400">FlashRank Neural Reranker</div>
                  <div className="text-slate-400 mt-1">Sub-20ms TinyBERT cross-encoder boosting candidate precision from 25 to top 5.</div>
                </div>
                <div className="bg-slate-900/60 p-3 rounded-lg border border-emerald-400/40">
                  <div className="font-bold text-emerald-400">FastMCP SSE Tool Server</div>
                  <div className="text-slate-400 mt-1">Type-safe JSON-RPC over Server-Sent Events exposing tools to Claude and Antigravity.</div>
                </div>
                <div className="bg-slate-900/60 p-3 rounded-lg border border-emerald-400/40">
                  <div className="font-bold text-emerald-400">Automated RAGAS Eval Gate</div>
                  <div className="text-slate-400 mt-1">CI test gate enforcing faithfulness &gt;= 0.90 across golden evaluation test cases.</div>
                </div>
              </div>
            </div>
          )}

          {selectedLayer === 'devops' && (
            <div className="space-y-3">
              <h4 className="text-sm font-bold text-white">Cloud DevOps & Stage Scout (Bumblebee)</h4>
              <p className="text-xs text-slate-300">
                Multi-stage Docker (&lt;180MB), AWS ECS Fargate task definitions, and offline demo.sh presentation fail-safe.
              </p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                <div className="bg-slate-900/60 p-3 rounded-lg border border-yellow-500/40">
                  <div className="font-bold text-yellow-400">Multi-Stage Dockerfile</div>
                  <div className="text-slate-400 mt-1">Slim Python 3.11 image under 180MB running with non-root appuser:appgroup.</div>
                </div>
                <div className="bg-slate-900/60 p-3 rounded-lg border border-yellow-500/40">
                  <div className="font-bold text-yellow-400">AWS ECS Fargate Architecture</div>
                  <div className="text-slate-400 mt-1">Serverless task definition with CloudWatch logs and auto-scaling to 4 tasks.</div>
                </div>
                <div className="bg-slate-900/60 p-3 rounded-lg border border-yellow-500/40">
                  <div className="font-bold text-yellow-400">Stage Fail-Safe Script (demo.sh)</div>
                  <div className="text-slate-400 mt-1">100% offline mock data script ensuring live stage demo never crashes if venue Wi-Fi drops.</div>
                </div>
                <div className="bg-slate-900/60 p-3 rounded-lg border border-yellow-500/40">
                  <div className="font-bold text-yellow-400">Marp Pitch Deck Engine</div>
                  <div className="text-slate-400 mt-1">Markdown-to-slides pipeline (pitch/pitch.marp.md) rendering high-contrast presentation decks.</div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
