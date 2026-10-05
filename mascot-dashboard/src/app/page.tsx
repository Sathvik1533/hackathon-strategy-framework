'use client';

import React, { useState } from 'react';
import { RoboticMascotChassis } from '@/components/RoboticMascotChassis';
import { AestheticSwitcher, AestheticType } from '@/components/AestheticSwitcher';
import { ArchitecturalDecisionCard } from '@/components/ArchitecturalDecisionCard';
import { TeammateOnboardingConsole } from '@/components/TeammateOnboardingConsole';
import { SkillsGrid } from '@/components/SkillsGrid';
import { RobotSquadOrchestrator } from '@/components/RobotSquadOrchestrator';
import { SkillFetcherConsole } from '@/components/SkillFetcherConsole';
import { MemoryTracerConsole } from '@/components/MemoryTracerConsole';
import { Terminal, Shield, Zap, Sparkles, ExternalLink, Github, BookOpen } from 'lucide-react';

export default function DashboardPage() {
  const [currentAesthetic, setCurrentAesthetic] = useState<AestheticType>('industrial-brutalism');
  const [telemetryMode, setTelemetryMode] = useState<'NOMINAL' | 'ANALYZING' | 'ALERT' | 'GUARDRAIL'>('NOMINAL');

  const handleAestheticChange = (aesthetic: AestheticType) => {
    setCurrentAesthetic(aesthetic);
    setTelemetryMode('ANALYZING');
    setTimeout(() => setTelemetryMode('NOMINAL'), 1500);
  };

  return (
    <main className="min-h-screen bg-[#070a0f] text-slate-100 p-4 md:p-8">
      {/* Top Navigation Bar */}
      <header className="max-w-7xl mx-auto flex flex-col md:flex-row items-start md:items-center justify-between pb-6 mb-8 border-b border-[#1c2738] gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-xl">🤖</span>
            <h1 className="text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2">
              ORBIT <span className="text-[#00f59b]">//</span> ROBOTIC MASCOT DIRECTOR
            </h1>
            <span className="bg-[#00f59b]/10 text-[#00f59b] border border-[#00f59b]/30 px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase">
              HSF v1.0 PROD
            </span>
          </div>
          <p className="text-xs text-slate-400 font-mono">
            Senior Principal Robotic Director • Transformers Robot Squad • Dynamic Skill Synthesizer • Continuous Learning Tracer
          </p>
        </div>

        <div className="flex items-center gap-3 text-xs font-mono">
          <a
            href="https://github.com/Sathvik1533/hackathon-strategy-framework"
            target="_blank"
            rel="noreferrer"
            className="flex items-center gap-1.5 bg-[#0d131f] hover:bg-[#151e30] border border-[#1c2738] px-3 py-2 rounded text-slate-300 transition-colors"
          >
            <Github className="w-4 h-4" /> REPOSITORY
          </a>
          <a
            href="http://localhost:8000/docs"
            target="_blank"
            rel="noreferrer"
            className="flex items-center gap-1.5 bg-[#00f59b] hover:bg-[#00d685] text-[#070a0f] font-bold px-3 py-2 rounded transition-colors"
          >
            <Terminal className="w-4 h-4" /> FASTAPI DOCS
          </a>
        </div>
      </header>

      {/* Main Grid Layout */}
      <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left Column: Robotic Mascot Chassis & Quick Telemetry (Cols: 4) */}
        <div className="lg:col-span-4 space-y-6">
          <RoboticMascotChassis
            statusText={`PAIRING ACTIVE // THEME: ${currentAesthetic.toUpperCase()}`}
            telemetryMode={telemetryMode}
          />

          {/* Quick CLI Execution Card */}
          <div className="bg-[#0d131f] border border-[#1c2738] rounded-lg p-5 font-mono text-xs">
            <div className="text-slate-400 font-bold mb-2 pb-2 border-b border-[#1c2738] flex items-center justify-between">
              <span>ORBIT DUAL ENGINES</span>
              <span className="text-[#00b4d8]">CLI RUNNERS</span>
            </div>
            <div className="space-y-2 text-[11px]">
              <div className="p-2 bg-[#05080e] rounded border border-[#141b27]">
                <div className="text-[#00f59b] font-bold">1. Transformers Squad CLI:</div>
                <code className="text-slate-300 block mt-0.5">
                  hsf squad &quot;&lt;problem&gt;&quot; --team-size 3
                </code>
              </div>
              <div className="p-2 bg-[#05080e] rounded border border-[#141b27]">
                <div className="text-[#00b4d8] font-bold">2. Dynamic Skill Fetcher:</div>
                <code className="text-slate-300 block mt-0.5">
                  hsf skill fetch stripe-payments
                </code>
              </div>
              <div className="p-2 bg-[#05080e] rounded border border-[#141b27]">
                <div className="text-purple-400 font-bold">3. Developer Memory Trace:</div>
                <code className="text-slate-300 block mt-0.5">
                  hsf memory
                </code>
              </div>
              <div className="p-2 bg-[#05080e] rounded border border-[#141b27]">
                <div className="text-amber-400 font-bold">4. Java Enterprise Director:</div>
                <code className="text-slate-300 block mt-0.5">
                  java -cp ai_layer/java HSFMascotDirector &quot;&lt;problem&gt;&quot;
                </code>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column: Orchestration, Decisions, Skills, Telemetry (Cols: 8) */}
        <div className="lg:col-span-8 space-y-8">
          {/* 1. Transformers Autonomous Robot Squad & Variable Team Orchestrator */}
          <RobotSquadOrchestrator />

          {/* 2. Autonomous Architectural Decision Card */}
          <ArchitecturalDecisionCard />

          {/* 3. Autonomous Frontend Aesthetic Matrix with Live Previews */}
          <AestheticSwitcher
            currentAesthetic={currentAesthetic}
            onSelectAesthetic={handleAestheticChange}
          />

          {/* 4. Dynamic Skill Registry & External Knowledge Synthesizer */}
          <SkillFetcherConsole />

          {/* 5. Senior Orbit Continuous Learning & Telemetry Stream */}
          <MemoryTracerConsole />

          {/* 6. Teammate Onboarding & Senior Desk */}
          <TeammateOnboardingConsole />

          {/* 7. Pre-Installed Skills Matrix */}
          <SkillsGrid />
        </div>
      </div>
    </main>
  );
}

