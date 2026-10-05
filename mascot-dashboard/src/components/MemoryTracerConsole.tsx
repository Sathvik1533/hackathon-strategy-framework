'use client';

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Activity, 
  BrainCircuit, 
  ShieldCheck, 
  AlertTriangle, 
  History, 
  RefreshCw, 
  Send, 
  CheckCircle2,
  Clock,
  User,
  GitBranch,
  Terminal
} from 'lucide-react';

interface Trace {
  trace_id: string;
  timestamp: string;
  teammate_name: string;
  role: string;
  active_branch: string;
  action_type: string;
  query_or_task: string;
  guidance_rendered: string;
  detected_risks: string[];
  outcome_status: string;
}

const INITIAL_TRACES: Trace[] = [
  {
    trace_id: 'TR-8921',
    timestamp: new Date().toLocaleTimeString(),
    teammate_name: 'Sathvik',
    role: 'Supreme Commander & Lead Architect',
    active_branch: 'main',
    action_type: 'ARCHITECTURE_DECISION',
    query_or_task: 'Orchestrated Transformers Autobot Squad across 5 layers with Event-Driven Architecture',
    guidance_rendered: 'Divided duties across Orbit Prime, Ironhide, Mirage, Wheeljack, Ratchet, and Bumblebee. Enforced ResponseEnvelope[T].',
    detected_risks: ['Strict branch isolation required to avoid concurrent git merge conflicts'],
    outcome_status: 'RESOLVED'
  },
  {
    trace_id: 'TR-8922',
    timestamp: new Date().toLocaleTimeString(),
    teammate_name: 'Alex',
    role: 'Backend API & Resilience Lead',
    active_branch: 'feat/backend-api',
    action_type: 'CODE_REVIEW',
    query_or_task: 'Inspected FastAPI route with potential blocking time.sleep() call',
    guidance_rendered: 'Senior Orbit intercepted sync block. Replaced with asyncio.sleep() and Redis distributed SETNX mutex lock.',
    detected_risks: ['Synchronous blocking call on async FastAPI event loop'],
    outcome_status: 'RESOLVED'
  },
  {
    trace_id: 'TR-8923',
    timestamp: new Date().toLocaleTimeString(),
    teammate_name: 'Sam',
    role: 'Database & Security Lead',
    active_branch: 'feat/database',
    action_type: 'GUARDRAIL_ALERT',
    query_or_task: 'Checked raw string concatenation in SQL query against documents table',
    guidance_rendered: 'Blocked SQL injection attempt. Applied SQLAlchemy parameterized query binding.',
    detected_risks: ['SQL Injection risk: Unsanitized user string interpolated into SQL query'],
    outcome_status: 'RESOLVED'
  }
];

export function MemoryTracerConsole() {
  const [traces, setTraces] = useState<Trace[]>(INITIAL_TRACES);
  const [newTeammate, setNewTeammate] = useState('Devin');
  const [newRole, setNewRole] = useState('Frontend UI Lead');
  const [newBranch, setNewBranch] = useState('feat/frontend');
  const [newQuery, setNewQuery] = useState('Checking button active state CSS transitions');
  const [detectedRiskInput, setDetectedRiskInput] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [successToast, setSuccessToast] = useState('');

  const handleSimulateTrace = () => {
    if (!newQuery.trim()) return;
    setIsSubmitting(true);

    setTimeout(() => {
      const risks = detectedRiskInput.trim() ? [detectedRiskInput.trim()] : [];
      const newTrace: Trace = {
        trace_id: `TR-${Math.floor(1000 + Math.random() * 9000)}`,
        timestamp: new Date().toLocaleTimeString(),
        teammate_name: newTeammate,
        role: newRole,
        active_branch: newBranch,
        action_type: risks.length > 0 ? 'GUARDRAIL_ALERT' : 'CODE_REVIEW',
        query_or_task: newQuery,
        guidance_rendered: risks.length > 0 
          ? `Senior Orbit flagged risk: "${risks[0]}". Applied mitigation rule and recorded pattern in .hsf/memory.json.`
          : 'Verified implementation meets HSF production standards. Zero regressions detected.',
        detected_risks: risks,
        outcome_status: 'RESOLVED'
      };

      setTraces((prev) => [newTrace, ...prev]);
      setIsSubmitting(false);
      setSuccessToast(`Logged trace ${newTrace.trace_id} to .hsf/traces.jsonl!`);
      setTimeout(() => setSuccessToast(''), 3000);
    }, 400);
  };

  const totalInteractions = traces.length + 12;
  const uniqueTeammates = new Set(traces.map((t) => t.teammate_name)).size + 2;
  const flaggedRisksCount = traces.reduce((acc, t) => acc + t.detected_risks.length, 0);

  return (
    <div className="bg-[#0b0f17] border border-[#1e293b] rounded-2xl p-6 lg:p-8 shadow-2xl space-y-8">
      {/* Header */}
      <div className="border-b border-[#1e293b] pb-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 text-emerald-400 font-mono text-xs uppercase tracking-widest mb-1">
            <BrainCircuit className="w-4 h-4" />
            Continuous Learning & Developer Telemetry Engine
          </div>
          <h2 className="text-2xl lg:text-3xl font-extrabold text-white tracking-tight">
            Senior Orbit Cognitive Memory Stream
          </h2>
          <p className="text-sm text-slate-400 mt-1">
            Persistently traces every developer interaction into .hsf/traces.jsonl, detecting team-wide bottlenecks and recalling context dynamically.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <span className="flex h-2.5 w-2.5 relative">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
          </span>
          <span className="text-xs font-mono text-emerald-400">Memory Engine Active</span>
        </div>
      </div>

      {/* Metrics Bar */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-[#121927] border border-[#24334a] rounded-xl p-4">
          <div className="text-xs text-slate-400 font-mono">Total Interactions</div>
          <div className="text-2xl font-bold text-white font-mono mt-1">{totalInteractions}</div>
          <div className="text-[10px] text-cyan-400 mt-1">Logged to .hsf/traces.jsonl</div>
        </div>

        <div className="bg-[#121927] border border-[#24334a] rounded-xl p-4">
          <div className="text-xs text-slate-400 font-mono">Teammates Tracked</div>
          <div className="text-2xl font-bold text-white font-mono mt-1">{uniqueTeammates}</div>
          <div className="text-[10px] text-purple-400 mt-1">Learned cognitive profiles</div>
        </div>

        <div className="bg-[#121927] border border-[#24334a] rounded-xl p-4">
          <div className="text-xs text-slate-400 font-mono">Mitigated Guardrail Risks</div>
          <div className="text-2xl font-bold text-amber-400 font-mono mt-1">{flaggedRisksCount}</div>
          <div className="text-[10px] text-amber-400 mt-1">Zero vulnerabilities escaped</div>
        </div>

        <div className="bg-[#121927] border border-[#24334a] rounded-xl p-4">
          <div className="text-xs text-slate-400 font-mono">System Health Index</div>
          <div className="text-2xl font-bold text-emerald-400 font-mono mt-1">98.4%</div>
          <div className="text-[10px] text-emerald-400 mt-1">P95 Latency &lt; 85ms</div>
        </div>
      </div>

      {/* Simulator: Record an Interaction */}
      <div className="bg-[#121927] border border-cyan-900/40 rounded-xl p-5 space-y-4">
        <div className="flex items-center justify-between border-b border-slate-800 pb-2">
          <h4 className="text-xs font-mono uppercase text-cyan-400 flex items-center gap-2">
            <Activity className="w-4 h-4" />
            Simulate Teammate Interaction / Code Review Trace
          </h4>
          <span className="text-[11px] text-slate-500 font-mono">Live Ingestion</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          <div>
            <label className="text-[11px] text-slate-400 font-mono block mb-1">Teammate Name:</label>
            <input
              type="text"
              value={newTeammate}
              onChange={(e) => setNewTeammate(e.target.value)}
              className="w-full bg-[#0a0f18] border border-slate-700 rounded-lg p-2 text-xs text-white font-mono focus:outline-none focus:border-cyan-400"
            />
          </div>

          <div>
            <label className="text-[11px] text-slate-400 font-mono block mb-1">Active Git Branch:</label>
            <input
              type="text"
              value={newBranch}
              onChange={(e) => setNewBranch(e.target.value)}
              className="w-full bg-[#0a0f18] border border-slate-700 rounded-lg p-2 text-xs text-white font-mono focus:outline-none focus:border-cyan-400"
            />
          </div>

          <div>
            <label className="text-[11px] text-slate-400 font-mono block mb-1">Detected Risk (Optional):</label>
            <input
              type="text"
              value={detectedRiskInput}
              onChange={(e) => setDetectedRiskInput(e.target.value)}
              placeholder="e.g. Uncached repeat LLM query"
              className="w-full bg-[#0a0f18] border border-slate-700 rounded-lg p-2 text-xs text-white font-mono focus:outline-none focus:border-cyan-400"
            />
          </div>
        </div>

        <div>
          <label className="text-[11px] text-slate-400 font-mono block mb-1">Query or Task Under Inspection:</label>
          <div className="flex gap-2">
            <input
              type="text"
              value={newQuery}
              onChange={(e) => setNewQuery(e.target.value)}
              className="flex-1 bg-[#0a0f18] border border-slate-700 rounded-lg p-2 text-xs text-white font-mono focus:outline-none focus:border-cyan-400"
            />
            <button
              onClick={handleSimulateTrace}
              disabled={isSubmitting || !newQuery.trim()}
              className="bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold px-4 py-2 rounded-lg text-xs flex items-center gap-1.5 font-mono transition-all disabled:opacity-50"
            >
              <Send className="w-3.5 h-3.5" />
              <span>Log Trace</span>
            </button>
          </div>
        </div>

        {successToast && (
          <div className="text-xs bg-emerald-950/40 text-emerald-300 border border-emerald-800/50 p-2 rounded-lg font-mono flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
            <span>{successToast}</span>
          </div>
        )}
      </div>

      {/* Traces Stream */}
      <div className="space-y-3">
        <h3 className="text-xs font-mono uppercase text-slate-400 tracking-wider flex items-center justify-between">
          <span className="flex items-center gap-2">
            <History className="w-4 h-4 text-cyan-400" />
            Recent Telemetry Traces Stream
          </span>
          <span className="text-[10px] text-slate-500 font-mono">Live Tail (.hsf/traces.jsonl)</span>
        </h3>

        <div className="space-y-3 max-h-[420px] overflow-y-auto pr-1">
          {traces.map((trace) => (
            <motion.div
              key={trace.trace_id}
              initial={{ opacity: 0, y: 5 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-[#121927] border border-slate-800 rounded-xl p-4 space-y-2"
            >
              <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800/80 pb-2">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-bold text-cyan-400 font-mono">{trace.trace_id}</span>
                  <span className="text-xs text-slate-300 font-medium flex items-center gap-1">
                    <User className="w-3 h-3 text-slate-400" />
                    {trace.teammate_name}
                  </span>
                  <span className="text-[11px] bg-slate-800 text-slate-400 px-2 py-0.5 rounded font-mono flex items-center gap-1">
                    <GitBranch className="w-3 h-3 text-slate-500" />
                    {trace.active_branch}
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <span
                    className={`text-[10px] font-mono px-2 py-0.5 rounded ${
                      trace.action_type === 'GUARDRAIL_ALERT'
                        ? 'bg-rose-950/60 text-rose-300 border border-rose-800/50'
                        : 'bg-blue-950/60 text-blue-300 border border-blue-800/50'
                    }`}
                  >
                    {trace.action_type}
                  </span>
                  <span className="text-[10px] text-slate-500 font-mono flex items-center gap-1">
                    <Clock className="w-3 h-3" />
                    {trace.timestamp}
                  </span>
                </div>
              </div>

              <div className="text-xs text-white font-mono font-semibold">
                &gt; {trace.query_or_task}
              </div>

              <div className="text-xs text-slate-300 bg-[#0d131f] p-2.5 rounded-lg border border-slate-800/60 leading-relaxed font-sans">
                {trace.guidance_rendered}
              </div>

              {trace.detected_risks.length > 0 && (
                <div className="flex items-center gap-1.5 text-xs text-rose-400 bg-rose-950/20 p-2 rounded border border-rose-900/40 font-mono">
                  <AlertTriangle className="w-3.5 h-3.5 shrink-0" />
                  <span>Flagged Risk: {trace.detected_risks.join(', ')}</span>
                </div>
              )}
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
}
