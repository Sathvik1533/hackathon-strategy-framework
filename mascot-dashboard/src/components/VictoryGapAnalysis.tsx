'use client';

import React, { useState } from 'react';
import { ShieldAlert, ShieldCheck, Terminal, Copy, Check, ExternalLink, Zap } from 'lucide-react';

interface VictoryGap {
  id: number;
  blindSpot: string;
  category: 'Stage & Demo' | 'AI & Cache' | 'Data & Search' | 'Infra & Cloud';
  layer: string;
  whyFail: string;
  howHsfWins: string;
  failSafeCommand: string;
  proofMetric: string;
}

const VICTORY_GAPS: VictoryGap[] = [
  {
    id: 1,
    blindSpot: '1. Conference Stage Wi-Fi Drop',
    category: 'Stage & Demo',
    layer: 'Presentation & Offline Resilience',
    whyFail: 'Live browser demo freezes because venue Wi-Fi is overloaded with 500 laptops. Judges walk away.',
    howHsfWins: 'HSF provides pitch/demo.sh, an offline terminal cURL script that runs entirely on localhost, delivering a 30-second live colored demo without internet.',
    failSafeCommand: 'bash pitch/demo.sh',
    proofMetric: '100% offline uptime, 0ms external network dependency'
  },
  {
    id: 2,
    blindSpot: '2. Upstream AI API Rate Limits & Latency',
    category: 'AI & Cache',
    layer: 'Backend & Resilience Layer',
    whyFail: 'LLM API provider throttles requests or takes 14 seconds to respond on stage, killing pitch momentum.',
    howHsfWins: 'HSF provides sub-10ms Redis Semantic Caching and Circuit Breakers. Repeated queries return in 8ms with zero upstream dependency.',
    failSafeCommand: 'curl -X POST http://localhost:8000/api/v1/agent/query',
    proofMetric: '8ms P95 cached latency, 3-state Circuit Breaker'
  },
  {
    id: 3,
    blindSpot: '3. Naive Vector Hallucination',
    category: 'Data & Search',
    layer: 'Database & RAG Pipeline',
    whyFail: 'Competitors use simple cosine search without reranking. When judges ask edge-case questions, the AI hallucinates.',
    howHsfWins: 'HSF combines HNSW vector search with BM25 keyword matching via RRF, followed by FlashRank neural cross-encoder reranking (<20ms). Faithfulness verified ≥0.90 with RAGAS.',
    failSafeCommand: 'python ai_layer/eval_ragas.py',
    proofMetric: 'RAGAS Faithfulness >= 0.90, FlashRank < 20ms'
  },
  {
    id: 4,
    blindSpot: '4. Unrestricted Agent Action Hazards',
    category: 'AI & Cache',
    layer: 'AI Multi-Agent Architecture',
    whyFail: 'Competitors let autonomous agents execute database writes or API deletions unchecked, crashing live on stage.',
    howHsfWins: 'HSF enforces a LangGraph Human-in-the-Loop Interrupt Gate (interrupt_before=["human_gate"]). Risky actions pause until authorized, demonstrating enterprise maturity.',
    failSafeCommand: 'python ai_layer/langgraph_supervisor.py',
    proofMetric: 'Zero unauthorized mutations, explicit approval checkpoint'
  },
  {
    id: 5,
    blindSpot: '5. Last-Minute Docker & Container Breakage',
    category: 'Infra & Cloud',
    layer: 'DevOps & Cloud Packaging',
    whyFail: 'Teams introduce dependencies or change Python versions at Hour 22. Container build fails at Hour 23:45.',
    howHsfWins: 'HSF provides a pre-verified multi-stage Docker build (<180MB) running as non-root appuser. The Dockerfile is tested from Minute 0 and never drifts.',
    failSafeCommand: 'docker build -f infra/Dockerfile -t hsf-core:latest .',
    proofMetric: 'Image size < 180MB, non-root appuser UID 10001'
  },
  {
    id: 6,
    blindSpot: '6. The Hour 23 Slide Rush',
    category: 'Stage & Demo',
    layer: 'Pitch Deck & Storytelling',
    whyFail: 'Teams spend 23 hours coding and scramble to build slides in Canva 15 minutes before judging, presenting an unpracticed mess.',
    howHsfWins: 'HSF includes pitch/pitch.marp.md pre-structured with the 6-minute formula (Hook, Problem, Archify Blueprint, Live Demo, Metrics, ROI). Teams draft slides at Hour 6 and compile to interactive HTML in 2 seconds.',
    failSafeCommand: 'bash pitch/generate_pitch.sh',
    proofMetric: '2-second Marp compilation to interactive HTML/PDF'
  },
  {
    id: 7,
    blindSpot: '7. Architecture Diagram Vagueness',
    category: 'Data & Search',
    layer: 'System Architecture & Blueprints',
    whyFail: 'Competitors show hand-drawn boxes with no verified ports, schemas, or protocols. Technical judges grill them on security.',
    howHsfWins: 'HSF provides Archify interactive SVG blueprints and full Mermaid.js topology maps displaying exact protocols, port mappings, and RLS policies.',
    failSafeCommand: 'open docs/architecture/system-architecture.html',
    proofMetric: 'Archify interactive SVG + Mermaid.js verified ports'
  }
];

export function VictoryGapAnalysis() {
  const [filter, setFilter] = useState<'All' | 'Stage & Demo' | 'AI & Cache' | 'Data & Search' | 'Infra & Cloud'>('All');
  const [copiedId, setCopiedId] = useState<number | null>(null);

  const filteredGaps = filter === 'All' 
    ? VICTORY_GAPS 
    : VICTORY_GAPS.filter(g => g.category === filter);

  const handleCopy = (id: number, text: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  return (
    <div className="bg-[#0b101b] border border-[#1c2738] rounded-xl p-6 font-mono">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between pb-4 border-b border-[#1c2738] gap-3">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-xl">🏆</span>
            <h2 className="text-lg font-bold text-white tracking-wide">
              5. What Else Are You Missing? The Hackathon Victory Gap Analysis
            </h2>
          </div>
          <p className="text-xs text-slate-400 mt-1 font-sans">
            Why 99% of teams fail on predictable technical, latency, and stage traps vs. how HSF systematically guarantees victory.
          </p>
        </div>

        <div className="flex items-center gap-1.5 bg-[#05080e] p-1 rounded-lg border border-[#141b27] self-start md:self-auto overflow-x-auto text-[11px]">
          {(['All', 'Stage & Demo', 'AI & Cache', 'Data & Search', 'Infra & Cloud'] as const).map(cat => (
            <button
              key={cat}
              onClick={() => setFilter(cat)}
              className={`px-2.5 py-1 rounded transition-colors whitespace-nowrap ${
                filter === cat
                  ? 'bg-[#00f59b] text-[#070a0f] font-bold'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      {/* Cards List */}
      <div className="mt-6 space-y-4">
        {filteredGaps.map(gap => (
          <div
            key={gap.id}
            className="bg-[#0e1626] border border-[#1e2d42] hover:border-[#2a3f5f] rounded-lg p-5 transition-all"
          >
            {/* Title & Badge */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-3 border-b border-[#182335]">
              <div className="flex items-center gap-2">
                <span className="text-amber-400 font-bold text-sm">{gap.blindSpot}</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="bg-[#141f33] text-slate-300 text-[10px] px-2 py-0.5 rounded border border-[#23334d]">
                  {gap.layer}
                </span>
                <span className="bg-[#00f59b]/10 text-[#00f59b] text-[10px] px-2 py-0.5 rounded border border-[#00f59b]/30">
                  {gap.category}
                </span>
              </div>
            </div>

            {/* Comparison Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 my-4 font-sans text-xs">
              {/* Failure Mode */}
              <div className="bg-[#1b1014] border border-[#3b1720] rounded-lg p-3.5">
                <div className="flex items-center gap-1.5 text-rose-400 font-bold mb-1.5 font-mono text-[11px]">
                  <ShieldAlert className="w-3.5 h-3.5 text-rose-400" />
                  <span>❌ WHY 99% OF TEAMS FAIL</span>
                </div>
                <p className="text-rose-200/90 leading-relaxed">
                  {gap.whyFail}
                </p>
              </div>

              {/* HSF Solution */}
              <div className="bg-[#0c1c17] border border-[#143d2c] rounded-lg p-3.5">
                <div className="flex items-center gap-1.5 text-emerald-400 font-bold mb-1.5 font-mono text-[11px]">
                  <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
                  <span>✔ HOW HSF ELIMINATES THE RISK</span>
                </div>
                <p className="text-emerald-200/90 leading-relaxed">
                  {gap.howHsfWins}
                </p>
              </div>
            </div>

            {/* Bottom Bar: Command & Proof Metric */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between bg-[#070b13] border border-[#141d2c] rounded p-2.5 gap-2 text-[11px]">
              <div className="flex items-center gap-2 text-slate-300 overflow-x-auto">
                <Terminal className="w-3.5 h-3.5 text-[#00b4d8] shrink-0" />
                <code className="text-cyan-300">{gap.failSafeCommand}</code>
                <button
                  onClick={() => handleCopy(gap.id, gap.failSafeCommand)}
                  className="p-1 hover:bg-[#151f30] rounded text-slate-400 hover:text-white transition-colors shrink-0"
                  title="Copy command"
                >
                  {copiedId === gap.id ? (
                    <Check className="w-3.5 h-3.5 text-emerald-400" />
                  ) : (
                    <Copy className="w-3.5 h-3.5" />
                  )}
                </button>
              </div>

              <div className="flex items-center gap-1.5 text-slate-400 self-end sm:self-auto shrink-0 font-mono text-[10px]">
                <Zap className="w-3 h-3 text-amber-400" />
                <span className="text-slate-300">{gap.proofMetric}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
