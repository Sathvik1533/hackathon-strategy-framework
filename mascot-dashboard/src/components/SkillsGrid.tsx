'use client';

import React from 'react';
import { Layers, ShieldCheck, Database, Cpu, Terminal, Presentation, Rocket } from 'lucide-react';

export const SkillsGrid: React.FC = () => {
  const skillCategories = [
    {
      layer: 'Frontend & UI Craft',
      icon: Layers,
      color: '#ec4899',
      skills: [
        { name: 'hallmark', desc: 'Anti-AI-slop design skill, typographic hierarchy & motion tokens' },
        { name: 'emil-design-eng', desc: 'Emil Kowalski UI polish, transform-only GPU animation rules' },
        { name: 'minimalist-ui', desc: 'Clean editorial-style interfaces, warm monochrome grids' },
      ],
    },
    {
      layer: 'Backend & API Architecture',
      icon: Terminal,
      color: '#00f59b',
      skills: [
        { name: 'fastapi-production-archetype', desc: 'Enterprise FastAPI structure, async lifespans, ResponseEnvelope' },
        { name: 'poetry-python-packaging', desc: 'Deterministic Python lockfiles and dependency isolation' },
        { name: 'context7-docs-fetcher', desc: 'Real-time library documentation scraper and contextualizer' },
      ],
    },
    {
      layer: 'Database & Hybrid Vector Search',
      icon: Database,
      color: '#00b4d8',
      skills: [
        { name: 'pgvector-hybrid-search', desc: 'PostgreSQL 16 HNSW Cosine + tsvector BM25 with RRF' },
        { name: 'agent-security-guardrails', desc: 'Supabase RLS multi-tenant policies and SQL injection prevention' },
      ],
    },
    {
      layer: 'AI / Multi-Agent Systems & Tools',
      icon: Cpu,
      color: '#a855f7',
      skills: [
        { name: 'langgraph-production-patterns', desc: 'Multi-agent supervisor graphs with human-in-the-loop gates' },
        { name: 'fastmcp-tool-server', desc: 'Model Context Protocol tool server over Server-Sent Events' },
        { name: 'pydantic-ai-workflows', desc: 'Type-safe agentic validation and structured outputs' },
        { name: 'rag-reranking-pipeline', desc: 'FlashRank cross-encoder reranking (top_k=5)' },
      ],
    },
    {
      layer: 'Resilience & Performance',
      icon: ShieldCheck,
      color: '#f59e0b',
      skills: [
        { name: 'async-agent-celery-redis', desc: 'Redis Streams pub/sub worker mesh and distributed task queues' },
        { name: 'llm-gateway-semantic-cache', desc: 'Sub-10ms Redis semantic caching bypassing redundant LLM calls' },
        { name: 'agent-eval-harness', desc: 'RAGAS 25-case golden dataset accuracy and faithfulness bench' },
      ],
    },
    {
      layer: 'DevOps & Pitch Presentation',
      icon: Presentation,
      color: '#ef4444',
      skills: [
        { name: 'agent-docker-aws-deploy', desc: 'Multi-stage Dockerfile (<180MB non-root) and AWS ECS Fargate' },
        { name: 'marp-presentation-engine', desc: 'Markdown-to-presentation generator for interactive HTML/PDF slides' },
        { name: 'hackathon-speedrun-kit', desc: '24-hour sprint milestones, emergency stage fail-safe runner' },
      ],
    },
  ];

  return (
    <div className="bg-[#0d131f] border border-[#1c2738] rounded-lg p-6 shadow-xl">
      <div className="flex items-center justify-between mb-4 pb-3 border-b border-[#1c2738]">
        <div className="flex items-center gap-2">
          <Layers className="w-5 h-5 text-[#a855f7]" />
          <h3 className="font-mono font-bold text-white text-base">
            PRE-INSTALLED SKILLS MATRIX (17 BATTLE-TESTED CAPABILITIES)
          </h3>
        </div>
        <span className="text-xs font-mono text-[#a855f7] bg-[#a855f7]/10 px-2.5 py-1 rounded border border-[#a855f7]/30">
          ALL LAYERS MAPPED
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {skillCategories.map((cat) => {
          const Icon = cat.icon;
          return (
            <div
              key={cat.layer}
              className="bg-[#05080e] border border-[#1c2738] rounded p-4 flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center gap-2 mb-3 pb-2 border-b border-[#1c2738]/60">
                  <Icon className="w-4 h-4" style={{ color: cat.color }} />
                  <span className="font-bold text-xs font-mono text-white">{cat.layer}</span>
                </div>
                <div className="space-y-2">
                  {cat.skills.map((s) => (
                    <div
                      key={s.name}
                      className="bg-[#0b101b] border border-[#141b27] p-2 rounded text-[11px]"
                    >
                      <div className="font-mono font-bold" style={{ color: cat.color }}>
                        `{s.name}`
                      </div>
                      <div className="text-slate-400 text-[10px] mt-0.5 leading-tight">
                        {s.desc}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
