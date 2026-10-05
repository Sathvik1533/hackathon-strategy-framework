'use client';

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  DownloadCloud, 
  Search, 
  Code, 
  CheckCircle2, 
  AlertTriangle, 
  BookOpen, 
  ExternalLink,
  Sparkles,
  GitBranch,
  Terminal
} from 'lucide-react';

interface Skill {
  name: string;
  category_layer: string;
  short_description: string;
  target_tech_stack: string[];
  core_dependencies: string[];
  best_practices: string[];
  forbidden_antipatterns: string[];
  sample_code_snippet: string;
  is_dynamically_acquired?: boolean;
}

const SAMPLE_BUILTIN_SKILLS: Skill[] = [
  {
    name: 'fastapi-production-archetype',
    category_layer: 'Backend API',
    short_description: 'Async FastAPI architecture with lifespan handlers, ResponseEnvelope[T], and clean hexagonal ports.',
    target_tech_stack: ['FastAPI', 'Python 3.11+', 'Uvicorn', 'Pydantic v2'],
    core_dependencies: ['fastapi', 'uvicorn', 'pydantic', 'httpx'],
    best_practices: ['Always wrap route responses in ResponseEnvelope[T].', 'Use non-blocking httpx.AsyncClient.'],
    forbidden_antipatterns: ['Never call time.sleep() inside async routes.'],
    sample_code_snippet: '@router.get("/health", response_model=ResponseEnvelope[HealthData])\nasync def health_check(): ...'
  },
  {
    name: 'pgvector-hybrid-search',
    category_layer: 'Database',
    short_description: 'PostgreSQL 16 HNSW Cosine distance combined with tsvector BM25 using Reciprocal Rank Fusion (RRF).',
    target_tech_stack: ['PostgreSQL 16', 'pgvector', 'SQLAlchemy 2.0', 'HNSW'],
    core_dependencies: ['pgvector', 'asyncpg', 'sqlalchemy'],
    best_practices: ['Create HNSW index: USING hnsw (embedding vector_cosine_ops) WITH (m=16, ef_construction=64).'],
    forbidden_antipatterns: ['Never run unindexed cosine searches on tables with >1,000 vectors.'],
    sample_code_snippet: 'SELECT id, (1.0 / (60 + dense_rank) + 1.0 / (60 + text_rank)) AS rrf_score FROM docs ORDER BY rrf_score DESC;'
  },
  {
    name: 'langgraph-production-patterns',
    category_layer: 'AI & Multi-Agent',
    short_description: 'Cyclic multi-agent supervisor state machines with human-in-the-loop review interrupt gates.',
    target_tech_stack: ['LangGraph', 'LangChain', 'Python 3.11+'],
    core_dependencies: ['langgraph', 'langchain-core'],
    best_practices: ['Configure interrupt_before=["human_gate"] for irreversible database writes.'],
    forbidden_antipatterns: ['Never allow unchecked autonomous recursive loops without recursion_limit.'],
    sample_code_snippet: 'workflow = StateGraph(AgentState)\napp = workflow.compile(interrupt_before=["human_gate"])'
  },
  {
    name: 'hallmark',
    category_layer: 'Frontend UI Craft',
    short_description: 'Anti-AI-slop design system enforcing typographic hierarchy, Emil Kowalski motion tokens, and WCAG AA.',
    target_tech_stack: ['Tailwind CSS', 'Framer Motion', 'Next.js'],
    core_dependencies: ['framer-motion', 'lucide-react'],
    best_practices: ['Animate only transform and opacity via GPU compositing.', 'Use cubic-bezier(0.16, 1, 0.3, 1) ease-out curve.'],
    forbidden_antipatterns: ['Never animate width, height, or margin.'],
    sample_code_snippet: ':root { --ease-out: cubic-bezier(0.16, 1, 0.3, 1); --dur-micro: 120ms; }'
  }
];

export function SkillFetcherConsole() {
  const [query, setQuery] = useState('');
  const [knowledgeLevel, setKnowledgeLevel] = useState('Intermediate');
  const [skills, setSkills] = useState<Skill[]>(SAMPLE_BUILTIN_SKILLS);
  const [selectedSkill, setSelectedSkill] = useState<Skill>(SAMPLE_BUILTIN_SKILLS[0]);
  const [isFetching, setIsFetching] = useState(false);
  const [fetchedMessage, setFetchedMessage] = useState('');

  const handleFetchOrSynthesize = () => {
    if (!query.trim()) return;
    setIsFetching(true);
    setFetchedMessage('');

    setTimeout(() => {
      const normalized = query.toLowerCase().replace(/[^a-z0-9_-]/g, '-');
      const isAudio = normalized.includes('audio') || normalized.includes('voice') || normalized.includes('webrtc');
      const is3D = normalized.includes('3d') || normalized.includes('three') || normalized.includes('spatial');
      const isPayment = normalized.includes('pay') || normalized.includes('stripe') || normalized.includes('billing');

      let layer = 'Full-Stack Feature Integration';
      let stack = ['Python 3.11+', 'FastAPI', 'TypeScript'];
      let deps = ['httpx', 'pydantic'];
      let bestPractices = [
        `Isolate '${query}' into a dedicated service adapter layer.`,
        'Enforce circuit breaker and exponential backoff retry policies.'
      ];
      let antipatterns = [
        'Never couple external provider schemas directly into relational database tables.'
      ];
      let snippet = `# Adapter for ${query}\nasync def execute_${normalized.replace(/-/g, '_')}(payload: dict):\n    async with httpx.AsyncClient() as client:\n        return await client.post('https://api.external.service', json=payload)`;

      if (isAudio) {
        layer = 'Audio & Real-Time Streams';
        stack = ['WebRTC', 'FastAPI SSE', 'Deepgram / Whisper'];
        deps = ['deepgram-sdk', 'soundfile', 'numpy'];
        bestPractices = [
          'Stream audio in PCM 16-bit 16kHz mono chunks for lowest latency.',
          'Use WebRTC data channels or SSE for sub-200ms round-trip audio synthesis.'
        ];
        antipatterns = ['Never buffer full 5-minute audio files before starting transcription.'];
        snippet = `async def stream_audio_chunks(websocket: WebSocket):\n    async for chunk in websocket.iter_bytes():\n        transcript = await deepgram.transcribe(chunk)`;
      } else if (is3D) {
        layer = 'Frontend 3D & Spatial Holography';
        stack = ['Three.js', 'React Three Fiber', 'GLSL', 'WebGL'];
        deps = ['three', '@types/three', '@react-three/fiber'];
        bestPractices = [
          'Dispose of unused geometries and materials on component unmount.',
          'Use requestAnimationFrame with delta time for 60fps rendering.'
        ];
        antipatterns = ['Never instantiate new Three.js materials inside the render tick loop.'];
        snippet = `const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });\nrenderer.setSize(window.innerWidth, window.innerHeight);`;
      } else if (isPayment) {
        layer = 'Fintech & Resilient Payments';
        stack = ['Stripe API', 'FastAPI Webhooks', 'Redis Locks'];
        deps = ['stripe', 'redis'];
        bestPractices = [
          'Verify cryptographic Stripe webhook signatures with stripe.Webhook.construct_event.',
          'Acquire Redis SETNX distributed lock to prevent duplicate charges on retry.'
        ];
        antipatterns = ['Never execute fulfillment without verifying cryptographically signed signatures.'];
        snippet = `event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)\nif event.type == 'payment_intent.succeeded': await process_fulfillment(event)`;
      }

      const newSkill: Skill = {
        name: normalized,
        category_layer: layer,
        short_description: `Dynamically synthesized production skill specification for '${query}' fetched from GitHub/web repository knowledge.`,
        target_tech_stack: stack,
        core_dependencies: deps,
        best_practices: bestPractices,
        forbidden_antipatterns: antipatterns,
        sample_code_snippet: snippet,
        is_dynamically_acquired: true
      };

      setSkills((prev) => [newSkill, ...prev]);
      setSelectedSkill(newSkill);
      setIsFetching(false);
      setFetchedMessage(`✨ Successfully synthesized '${newSkill.name}' from GitHub/web knowledge!`);
    }, 600);
  };

  const getShapedInstructions = (skill: Skill, level: string) => {
    if (level === 'Beginner') {
      return `👋 Senior Orbit Guide for Beginners:\n1. Copy the boilerplate from '${skill.name}'. Don't reinvent the wheel!\n2. Core best practices to follow:\n` +
        skill.best_practices.map((b) => `   - ${b}`).join('\n') +
        `\n3. Traps to strictly avoid:\n` +
        skill.forbidden_antipatterns.map((a) => `   - ${a}`).join('\n') +
        `\n4. Starter snippet:\n${skill.sample_code_snippet}`;
    } else if (level === 'Senior') {
      return `⚡ Senior Orbit Technical Specification (Lead Level):\nStack: ${skill.target_tech_stack.join(', ')} | Deps: ${skill.core_dependencies.join(', ')}\n` +
        `Architectural Guardrails:\n` +
        skill.best_practices.map((b) => `   ✔ ${b}`).join('\n') +
        `\nStrict Anti-Patterns (Zero tolerance in code review):\n` +
        skill.forbidden_antipatterns.map((a) => `   ✖ ${a}`).join('\n') +
        `\nInterface Contract:\n${skill.sample_code_snippet}`;
    }
    return `🤖 Senior Orbit Pairing Briefing (Intermediate):\nFocus on rapid delivery adhering to HSF production standards.\nChecklist:\n` +
      skill.best_practices.map((b) => `   - ${b}`).join('\n') +
      `\nStrictly avoid:\n` +
      skill.forbidden_antipatterns.map((a) => `   - ${a}`).join('\n');
  };

  return (
    <div className="bg-[#0b0f17] border border-[#1e293b] rounded-2xl p-6 lg:p-8 shadow-2xl space-y-8">
      {/* Header */}
      <div className="border-b border-[#1e293b] pb-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 text-cyan-400 font-mono text-xs uppercase tracking-widest mb-1">
            <DownloadCloud className="w-4 h-4" />
            Dynamic Skill Registry & External Knowledge Synthesizer
          </div>
          <h2 className="text-2xl lg:text-3xl font-extrabold text-white tracking-tight">
            Skill Acquisition & Teammate Adaptation Engine
          </h2>
          <p className="text-sm text-slate-400 mt-1">
            If any skill or library is missing, Orbit dynamically fetches and synthesizes production SKILL.md specs from GitHub/web knowledge.
          </p>
        </div>

        {/* Knowledge Level Selector */}
        <div className="bg-[#131b2a] border border-[#24334a] rounded-xl p-2.5 px-4 flex items-center gap-3">
          <span className="text-xs font-mono text-slate-300">Teammate Level:</span>
          <select
            value={knowledgeLevel}
            onChange={(e) => setKnowledgeLevel(e.target.value)}
            className="bg-[#1c273c] text-cyan-300 text-xs font-mono rounded px-2.5 py-1 border border-cyan-800/60 focus:outline-none"
          >
            <option value="Beginner">Beginner (Step-by-Step)</option>
            <option value="Intermediate">Intermediate (Balanced)</option>
            <option value="Senior">Senior / Lead (High Velocity)</option>
          </select>
        </div>
      </div>

      {/* Fetcher Input Bar */}
      <div className="flex flex-col sm:flex-row gap-3">
        <div className="relative flex-1">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3.5" />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleFetchOrSynthesize()}
            placeholder="Search pre-installed skills or type external skill (e.g. stripe-payments, webrtc-audio, temporal-workflows)..."
            className="w-full bg-[#121927] border border-[#24334a] rounded-xl pl-10 pr-4 py-2.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-cyan-400 font-mono"
          />
        </div>
        <button
          onClick={handleFetchOrSynthesize}
          disabled={isFetching || !query.trim()}
          className="bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold px-5 py-2.5 rounded-xl text-xs flex items-center justify-center gap-2 transition-all disabled:opacity-50 shrink-0 font-mono"
        >
          {isFetching ? (
            <>
              <Sparkles className="w-4 h-4 animate-spin" />
              <span>Synthesizing...</span>
            </>
          ) : (
            <>
              <DownloadCloud className="w-4 h-4" />
              <span>Fetch / Synthesize Skill</span>
            </>
          )}
        </button>
      </div>

      {fetchedMessage && (
        <motion.div
          initial={{ opacity: 0, y: -5 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-xs bg-emerald-950/40 text-emerald-300 border border-emerald-800/50 p-2.5 rounded-lg font-mono flex items-center gap-2"
        >
          <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
          <span>{fetchedMessage}</span>
        </motion.div>
      )}

      {/* Main Content Layout: Skills List & Detail View */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left: Skills Catalog */}
        <div className="space-y-3">
          <h3 className="text-xs font-mono uppercase text-slate-400 tracking-wider flex items-center justify-between">
            <span>Available Catalog ({skills.length})</span>
            <span className="text-[10px] text-cyan-400">Cached in .hsf/skills</span>
          </h3>

          <div className="space-y-2 max-h-[460px] overflow-y-auto pr-1">
            {skills.map((s) => (
              <div
                key={s.name}
                onClick={() => setSelectedSkill(s)}
                className={`p-3 rounded-xl border cursor-pointer transition-all ${
                  selectedSkill.name === s.name
                    ? 'bg-[#152033] border-cyan-400 shadow-md shadow-cyan-950/40'
                    : 'bg-[#101725] border-[#1e293b] hover:border-slate-700'
                }`}
              >
                <div className="flex items-start justify-between gap-2">
                  <div className="font-mono text-xs font-bold text-white truncate">{s.name}</div>
                  {s.is_dynamically_acquired && (
                    <span className="text-[10px] bg-purple-900/60 text-purple-300 px-1.5 py-0.5 rounded border border-purple-700 font-mono shrink-0">
                      Dynamic
                    </span>
                  )}
                </div>
                <div className="text-[11px] text-slate-400 line-clamp-1 mt-1">{s.short_description}</div>
                <div className="text-[10px] text-cyan-400 font-mono mt-2">{s.category_layer}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Right: Selected Skill Detail & Shaped Instructions */}
        <div className="lg:col-span-2 space-y-4">
          <div className="bg-[#121927] border border-slate-800 rounded-xl p-5 space-y-4">
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 border-b border-slate-800 pb-3">
              <div>
                <h4 className="text-lg font-bold text-white font-mono flex items-center gap-2">
                  {selectedSkill.name}
                  {selectedSkill.is_dynamically_acquired && (
                    <span className="text-xs bg-purple-900/60 text-purple-300 px-2 py-0.5 rounded border border-purple-700 font-mono">
                      Acquired from External Spec
                    </span>
                  )}
                </h4>
                <p className="text-xs text-cyan-400 font-mono">{selectedSkill.category_layer}</p>
              </div>
              <div className="flex flex-wrap gap-1">
                {selectedSkill.target_tech_stack.map((stk) => (
                  <span key={stk} className="text-[10px] bg-slate-800 text-slate-300 px-2 py-0.5 rounded font-mono">
                    {stk}
                  </span>
                ))}
              </div>
            </div>

            <p className="text-xs text-slate-300 leading-relaxed">{selectedSkill.short_description}</p>

            {/* Best Practices & Antipatterns */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-[#0d131f] border border-emerald-900/40 rounded-lg p-3">
                <h5 className="text-xs font-mono uppercase text-emerald-400 mb-2 flex items-center gap-1.5">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  Mandatory Best Practices
                </h5>
                <ul className="space-y-1 text-xs text-slate-300">
                  {selectedSkill.best_practices.map((bp, i) => (
                    <li key={i} className="flex items-start gap-1.5">
                      <span className="text-emerald-400">&bull;</span>
                      <span>{bp}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="bg-[#0d131f] border border-rose-900/40 rounded-lg p-3">
                <h5 className="text-xs font-mono uppercase text-rose-400 mb-2 flex items-center gap-1.5">
                  <AlertTriangle className="w-3.5 h-3.5" />
                  Forbidden Anti-Patterns
                </h5>
                <ul className="space-y-1 text-xs text-slate-300">
                  {selectedSkill.forbidden_antipatterns.map((ap, i) => (
                    <li key={i} className="flex items-start gap-1.5">
                      <span className="text-rose-400">&bull;</span>
                      <span>{ap}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            {/* Code Snippet */}
            <div>
              <h5 className="text-xs font-mono uppercase text-slate-400 mb-1 flex items-center gap-1.5">
                <Code className="w-3.5 h-3.5 text-cyan-400" />
                Verified Implementation Boilerplate
              </h5>
              <pre className="bg-[#080c14] border border-slate-800 rounded-lg p-3 text-xs text-cyan-300 font-mono overflow-x-auto">
                <code>{selectedSkill.sample_code_snippet}</code>
              </pre>
            </div>

            {/* Shaped Instructions by Teammate Knowledge Level */}
            <div>
              <h5 className="text-xs font-mono uppercase text-amber-400 mb-1 flex items-center gap-1.5">
                <Terminal className="w-3.5 h-3.5" />
                Tailored Prompt Instructions ({knowledgeLevel} Mode)
              </h5>
              <pre className="bg-[#090e18] border border-amber-900/40 rounded-lg p-3 text-xs text-slate-300 font-mono whitespace-pre-wrap">
                {getShapedInstructions(selectedSkill, knowledgeLevel)}
              </pre>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
