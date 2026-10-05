'use client';

import React, { useState } from 'react';
import { UserCheck, GitBranch, ShieldAlert, CheckCircle, Copy, Check, Terminal, Sparkles } from 'lucide-react';

export const TeammateOnboardingConsole: React.FC = () => {
  const [name, setName] = useState('Sathvik');
  const [role, setRole] = useState('Backend API, Data Pipeline & Resilience Lead');
  const [branch, setBranch] = useState('feat/backend-api');
  const [knowledge, setKnowledge] = useState('Advanced');
  const [aiIde, setAiIde] = useState('Antigravity');
  const [goal, setGoal] = useState('Implement sub-10ms Redis semantic cache & Circuit Breaker policies');
  const [copied, setCopied] = useState(false);
  const [briefingReady, setBriefingReady] = useState(false);

  const roles = [
    'Backend API, Data Pipeline & Resilience Lead',
    'Frontend UI, Design System & Real-Time Interaction Lead',
    'AI / Multi-Agent Systems & Vector Search Lead',
    'Database Schema, pgvector & Supabase RLS Lead',
    'Cloud DevOps, CI/CD, Pitch Deck & Live Demo Lead',
  ];

  const ides = ['Antigravity', 'Claude 3.7 Sonnet', 'Cursor', 'Windsurf', 'Hero Agent'];

  const getBranchForRole = (r: string) => {
    if (r.includes('Backend')) return 'feat/backend-api';
    if (r.includes('Frontend')) return 'feat/frontend-ui';
    if (r.includes('AI')) return 'feat/langgraph-supervisor';
    if (r.includes('Database')) return 'feat/database-rls';
    return 'feat/devops-pitch';
  };

  const handleRoleChange = (newRole: string) => {
    setRole(newRole);
    setBranch(getBranchForRole(newRole));
  };

  const generatedPrompt = `### SQUAD MEMBER: ${name} (${role})
### AGENTIC AI IDE: ${aiIde}
### KNOWLEDGE LEVEL: ${knowledge}
### ACTIVE BRANCH: \`${branch}\`
### CONTRIBUTION GOAL: ${goal}

Instructions for ${aiIde}:
1. You are paired with Senior Orbit (Senior Principal Robotic Director).
2. Respect all HSF architecture standards in this repository.
3. Strict Guardrails:
   - NEVER write blocking synchronous calls in async FastAPI routes.
   - NEVER return unvalidated JSON dictionaries without Pydantic schema validation.
   - NEVER bypass Circuit Breaker protection on third-party APIs.
   - NEVER run production Docker containers as root.
4. Immediate Actions:
   - Inspect existing template files on branch \`${branch}\`.
   - Implement assigned tasks ensuring 100% test passing rate.
   - Run 'ruff check --fix . && pytest && python3 scripts/review_pr.py' before any git push.`;

  const copyPrompt = () => {
    navigator.clipboard.writeText(generatedPrompt);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="bg-[#0d131f] border border-[#1c2738] rounded-lg p-6 shadow-xl">
      <div className="flex items-center justify-between mb-4 pb-3 border-b border-[#1c2738]">
        <div className="flex items-center gap-2">
          <UserCheck className="w-5 h-5 text-[#00b4d8]" />
          <h3 className="font-mono font-bold text-white text-base">
            TEAMMATE ONBOARDING & SENIOR DESK
          </h3>
        </div>
        <span className="text-xs font-mono text-[#00f59b] bg-[#00f59b]/10 px-2.5 py-1 rounded border border-[#00f59b]/30">
          SENIOR ORBIT PAIRING
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-5">
        <div>
          <label className="block text-xs font-mono text-slate-400 mb-1">TEAMMATE NAME</label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="w-full bg-[#05080e] border border-[#1c2738] rounded p-2.5 text-sm font-mono text-white focus:border-[#00b4d8] focus:outline-none"
          />
        </div>

        <div>
          <label className="block text-xs font-mono text-slate-400 mb-1">ASSIGNED SQUAD ROLE</label>
          <select
            value={role}
            onChange={(e) => handleRoleChange(e.target.value)}
            className="w-full bg-[#05080e] border border-[#1c2738] rounded p-2.5 text-sm font-mono text-white focus:border-[#00b4d8] focus:outline-none"
          >
            {roles.map((r) => (
              <option key={r} value={r}>
                {r}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-xs font-mono text-slate-400 mb-1">ACTIVE GIT BRANCH</label>
          <input
            type="text"
            value={branch}
            onChange={(e) => setBranch(e.target.value)}
            className="w-full bg-[#05080e] border border-[#1c2738] rounded p-2.5 text-sm font-mono text-[#00f59b] focus:border-[#00b4d8] focus:outline-none"
          />
        </div>

        <div>
          <label className="block text-xs font-mono text-slate-400 mb-1">PRIMARY AGENTIC AI IDE</label>
          <select
            value={aiIde}
            onChange={(e) => setAiIde(e.target.value)}
            className="w-full bg-[#05080e] border border-[#1c2738] rounded p-2.5 text-sm font-mono text-white focus:border-[#00b4d8] focus:outline-none"
          >
            {ides.map((ide) => (
              <option key={ide} value={ide}>
                {ide}
              </option>
            ))}
          </select>
        </div>

        <div className="md:col-span-2">
          <label className="block text-xs font-mono text-slate-400 mb-1">YOUR KEY CONTRIBUTION GOAL</label>
          <input
            type="text"
            value={goal}
            onChange={(e) => setGoal(e.target.value)}
            className="w-full bg-[#05080e] border border-[#1c2738] rounded p-2.5 text-sm font-mono text-white focus:border-[#00b4d8] focus:outline-none"
          />
        </div>
      </div>

      <button
        onClick={() => setBriefingReady(true)}
        className="w-full bg-[#00b4d8] hover:bg-[#0096c7] text-[#070a0f] font-mono font-bold py-2.5 rounded text-xs uppercase tracking-wider transition-colors mb-5"
      >
        GENERATE PERSONALIZED BRIEFING & AI IDE PROMPT
      </button>

      {/* Output Briefing Card */}
      {briefingReady && (
        <div className="bg-[#05080e] border border-[#1c2738] rounded p-5 space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-[#1c2738]">
            <div className="flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-[#00f59b]" />
              <span className="font-mono text-xs font-bold text-white">
                SENIOR BRIEFING FOR {name.toUpperCase()} (BRANCH: {branch})
              </span>
            </div>
            <button
              onClick={copyPrompt}
              className="flex items-center gap-1.5 bg-[#141d2e] hover:bg-[#1a263c] text-xs font-mono text-[#00f59b] px-3 py-1.5 rounded border border-[#00f59b]/30 transition-all"
            >
              {copied ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
              {copied ? 'COPIED TO CLIPBOARD!' : 'COPY PROMPT FOR AI IDE'}
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="border border-[#10b981]/30 bg-[#10b981]/5 p-3 rounded">
              <h4 className="text-xs font-mono font-bold text-[#10b981] mb-2 flex items-center gap-1">
                <CheckCircle className="w-3.5 h-3.5" /> WHAT TO DO (SENIOR DOs):
              </h4>
              <ul className="text-[11px] text-slate-300 space-y-1 font-mono list-disc list-inside">
                <li>Follow the single-responsibility principle per file.</li>
                <li>Write async handlers with typed ResponseEnvelope wrappers.</li>
                <li>Verify p95 latency remains below 300ms.</li>
                <li>Run automated tests before pushing commits.</li>
              </ul>
            </div>

            <div className="border border-[#ef4444]/30 bg-[#ef4444]/5 p-3 rounded">
              <h4 className="text-xs font-mono font-bold text-[#ef4444] mb-2 flex items-center gap-1">
                <ShieldAlert className="w-3.5 h-3.5" /> CRITICAL GUARDRAILS (WHAT NOT TO DO):
              </h4>
              <ul className="text-[11px] text-slate-300 space-y-1 font-mono list-disc list-inside">
                <li>NO synchronous time.sleep() or requests inside async routes.</li>
                <li>NO raw SQL string concatenation (SQL injection risk).</li>
                <li>NO unprotected external API calls without Circuit Breakers.</li>
                <li>NO running Docker containers as root user in production.</li>
              </ul>
            </div>
          </div>

          {/* Generated IDE Prompt Preview */}
          <div>
            <div className="text-[11px] font-mono text-slate-400 mb-1.5">
              CUSTOM PROMPT FOR {aiIde.toUpperCase()}:
            </div>
            <pre className="bg-[#0b101b] border border-[#141b27] p-3 rounded font-mono text-[11px] text-[#00b4d8] whitespace-pre-wrap overflow-x-auto max-h-48">
              {generatedPrompt}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
};
