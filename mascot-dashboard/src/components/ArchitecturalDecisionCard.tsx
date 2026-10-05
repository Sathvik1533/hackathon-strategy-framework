'use client';

import React, { useState } from 'react';
import { Cpu, CheckCircle2, XCircle, ArrowRight, Server, Database, Layers } from 'lucide-react';

interface PatternData {
  patternName: string;
  architecturalStyle: string;
  whyChosen: string;
  whyNotMicroservices: string;
  whyNotSimpleMonolith: string;
}

export const ArchitecturalDecisionCard: React.FC = () => {
  const [problemStatement, setProblemStatement] = useState(
    'Real-time IoT drone fleet collision avoidance telemetry & automated dispatch'
  );
  const [loading, setLoading] = useState(false);
  const [decision, setDecision] = useState<PatternData>({
    patternName: 'Event-Driven Architecture (EDA) with Asynchronous Redis Streams & CQRS Light',
    architecturalStyle: 'Decoupled Event-Driven Pipeline + Asynchronous Worker Mesh',
    whyChosen:
      'High-ingestion event streams and telemetry require immediate sub-5ms command acknowledgment without blocking read query threads. Decoupling command writes via Redis queues ensures that abrupt bursts in sensor signals or transaction spikes never degrade browser dashboard responsiveness.',
    whyNotMicroservices:
      'Pure microservices introduce distributed network latency, cross-service auth token exchanges, Docker Compose network routing headaches, and distributed tracing complexity that reliably derails teams in a 24-hour sprint. A modular event-bus in a single codebase provides the same decoupling benefits with zero deployment overhead.',
    whyNotSimpleMonolith:
      'A naive monolithic request/response loop blocks the single-threaded asyncio event loop during prolonged LLM or embedding calls, resulting in HTTP 504 Gateway Timeouts on stage.',
  });

  const handleEvaluate = async () => {
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/api/v1/agent/pattern-decision', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ problem_statement: problemStatement }),
      });
      if (res.ok) {
        const json = await res.json();
        const data = json.data;
        setDecision({
          patternName: data.pattern_name,
          architecturalStyle: data.architectural_style,
          whyChosen: data.why_chosen,
          whyNotMicroservices: data.why_not_microservices,
          whyNotSimpleMonolith: data.why_not_simple_monolith,
        });
      }
    } catch (err) {
      // Local fallback logic if backend server is not active
      const p = problemStatement.toLowerCase();
      if (p.includes('health') || p.includes('legal') || p.includes('agent')) {
        setDecision({
          patternName: 'Modular Monolith with Hexagonal Ports & Adapters + FastMCP Tool Isolation',
          architecturalStyle: 'Hexagonal Architecture (Clean Architecture / Ports & Adapters)',
          whyChosen:
            'Complex multi-agent reasoning and sensitive domain rules require strict isolation between core business logic, external LLM model providers, and third-party tools.',
          whyNotMicroservices:
            'Splitting every agent and tool into independent containers causes severe version drift and fragile deployment pipelines that waste crucial hackathon hours.',
          whyNotSimpleMonolith:
            'Tightly coupling LLM prompts with direct database queries creates brittle spaghetti code where modifying a database column breaks agent reasoning nodes.',
        });
      } else {
        setDecision({
          patternName: 'Event-Driven Architecture (EDA) with Asynchronous Redis Streams & CQRS Light',
          architecturalStyle: 'Decoupled Event-Driven Pipeline + Asynchronous Worker Mesh',
          whyChosen:
            'High-ingestion event streams and telemetry require immediate sub-5ms command acknowledgment without blocking read query threads.',
          whyNotMicroservices:
            'Microservices introduce network latency and deployment complexity that consumes valuable sprint time.',
          whyNotSimpleMonolith:
            'A naive monolithic request/response loop blocks the asyncio event loop during prolonged LLM calls.',
        });
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-[#0d131f] border border-[#1c2738] rounded-lg p-6 shadow-xl">
      <div className="flex items-center justify-between mb-4 pb-3 border-b border-[#1c2738]">
        <div className="flex items-center gap-2">
          <Cpu className="w-5 h-5 text-[#00f59b]" />
          <h3 className="font-mono font-bold text-white text-base">
            AUTONOMOUS ARCHITECTURAL DECISION ENGINE
          </h3>
        </div>
        <span className="text-xs font-mono text-[#00f59b] bg-[#00f59b]/10 px-2.5 py-1 rounded border border-[#00f59b]/30">
          PARENT AGENT DIRECTIVE
        </span>
      </div>

      <div className="mb-4">
        <label className="block text-xs font-mono text-slate-400 mb-1.5">
          ENTER YOUR HACKATHON PROBLEM STATEMENT:
        </label>
        <div className="flex gap-2">
          <input
            type="text"
            value={problemStatement}
            onChange={(e) => setProblemStatement(e.target.value)}
            className="flex-1 bg-[#05080e] border border-[#1c2738] rounded p-2.5 text-xs font-mono text-white focus:border-[#00f59b] focus:outline-none"
            placeholder="e.g. AI-Powered Autonomous Clinical Diagnostics & Multi-Agent Trials"
          />
          <button
            onClick={handleEvaluate}
            disabled={loading}
            className="bg-[#00f59b] hover:bg-[#00d685] text-[#070a0f] font-mono font-bold px-5 py-2.5 rounded text-xs uppercase tracking-wider transition-colors disabled:opacity-50"
          >
            {loading ? 'ANALYZING...' : 'EVALUATE PATTERN'}
          </button>
        </div>
      </div>

      {/* Selected Architectural Pattern Output Card */}
      <div className="bg-[#05080e] border border-[#1c2738] rounded-lg p-5">
        <div className="mb-4">
          <div className="text-[11px] font-mono text-slate-400 mb-1">SELECTED ARCHITECTURAL PATTERN:</div>
          <h4 className="text-base font-bold text-[#00f59b] font-mono flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-[#00f59b]" />
            {decision.patternName}
          </h4>
          <div className="text-xs font-mono text-[#00b4d8] mt-0.5">
            STYLE: {decision.architecturalStyle}
          </div>
        </div>

        <div className="space-y-3 text-xs leading-relaxed">
          <div className="p-3 bg-[#0b101b] border border-[#141b27] rounded">
            <span className="font-bold text-white block mb-1">🎯 Why Orbit Chose This Pattern:</span>
            <p className="text-slate-300 font-mono text-[11px]">{decision.whyChosen}</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            <div className="p-3 bg-[#130d10] border border-[#ef4444]/30 rounded">
              <span className="font-bold text-[#ef4444] block mb-1 flex items-center gap-1">
                <XCircle className="w-3.5 h-3.5" /> Why Microservices Were Rejected:
              </span>
              <p className="text-slate-300 font-mono text-[11px]">{decision.whyNotMicroservices}</p>
            </div>

            <div className="p-3 bg-[#13110d] border border-[#f59e0b]/30 rounded">
              <span className="font-bold text-[#f59e0b] block mb-1 flex items-center gap-1">
                <XCircle className="w-3.5 h-3.5" /> Why Simple Monolith Was Rejected:
              </span>
              <p className="text-slate-300 font-mono text-[11px]">{decision.whyNotSimpleMonolith}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
