'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Palette, CheckCircle2, Sparkles, Sliders, Box, Layers, Terminal } from 'lucide-react';

export type AestheticType =
  | 'industrial-brutalism'
  | 'neo-brutalism'
  | 'glassmorphism'
  | 'claymorphism'
  | 'skeuomorphism';

interface AestheticSwitcherProps {
  currentAesthetic: AestheticType;
  onSelectAesthetic: (aesthetic: AestheticType) => void;
}

export const AestheticSwitcher: React.FC<AestheticSwitcherProps> = ({
  currentAesthetic,
  onSelectAesthetic,
}) => {
  const aesthetics = [
    {
      id: 'industrial-brutalism' as AestheticType,
      name: 'Industrial Brutalism',
      badge: 'SYSTEM HUD',
      icon: Terminal,
      archetype: 'High-Density Monospace Grid, Obsidian Surfaces & Phosphor LEDs',
      fitFor: 'Developer Tools, Cloud Infra, Cybersecurity, AI Observability',
      color: '#00f59b',
    },
    {
      id: 'neo-brutalism' as AestheticType,
      name: 'Neo-Brutalism',
      badge: 'BOLD POP',
      icon: Box,
      archetype: '3px Solid Black Borders, 4px Hard Offset Shadows & Pop Yellow/Pink',
      fitFor: 'B2C Consumer, Viral Creator Economy, Web3, Gaming Hackathons',
      color: '#facc15',
    },
    {
      id: 'glassmorphism' as AestheticType,
      name: 'Glassmorphism',
      badge: 'FROSTED GLASS',
      icon: Layers,
      archetype: 'Multi-Tiered Frosted Glass, Hairline Specular Borders & Radial Glows',
      fitFor: 'Healthcare Clinical RAG, Legal Governance, Executive AI Copilots',
      color: '#38bdf8',
    },
    {
      id: 'claymorphism' as AestheticType,
      name: 'Claymorphism',
      badge: 'SOFT 3D',
      icon: Sparkles,
      archetype: 'Pillowy Rounded Cards (28px Radius) & Dual Inset Tactile Shadows',
      fitFor: 'EdTech, Children Math Tutors, Habit Trackers, Friendly Wellness',
      color: '#ec4899',
    },
    {
      id: 'skeuomorphism' as AestheticType,
      name: 'Skeuomorphism',
      badge: 'ANALOG HARDWARE',
      icon: Sliders,
      archetype: 'Brushed Titanium, Embossed Knobs, Recessed Meters & Tube LED Glows',
      fitFor: 'Audio Synthesizers, Hardware Simulators, DSP Mixing Consoles',
      color: '#ff851b',
    },
  ];

  return (
    <div className="bg-[#0d131f] border border-[#1c2738] rounded-lg p-6 shadow-xl">
      <div className="flex items-center justify-between mb-4 pb-3 border-b border-[#1c2738]">
        <div className="flex items-center gap-2">
          <Palette className="w-5 h-5 text-[#00f59b]" />
          <h3 className="font-mono font-bold text-white text-base">
            AUTONOMOUS FRONTEND AESTHETIC MATRIX
          </h3>
        </div>
        <span className="text-xs font-mono text-[#00b4d8] bg-[#00b4d8]/10 px-2.5 py-1 rounded border border-[#00b4d8]/30">
          5 PRODUCTION PARADIGMS
        </span>
      </div>

      {/* Aesthetic Selector Tabs */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-2 mb-6">
        {aesthetics.map((item) => {
          const Icon = item.icon;
          const isSelected = currentAesthetic === item.id;
          return (
            <button
              key={item.id}
              onClick={() => onSelectAesthetic(item.id)}
              className={`p-3 rounded text-left transition-all relative flex flex-col justify-between ${
                isSelected
                  ? 'bg-[#141d2e] border-2 shadow-lg'
                  : 'bg-[#080c14] border border-[#1c2738] hover:border-slate-500 opacity-80 hover:opacity-100'
              }`}
              style={{ borderColor: isSelected ? item.color : undefined }}
            >
              <div>
                <div className="flex items-center justify-between mb-1.5">
                  <Icon className="w-4 h-4" style={{ color: item.color }} />
                  {isSelected && <CheckCircle2 className="w-3.5 h-3.5" style={{ color: item.color }} />}
                </div>
                <div className="font-bold text-xs text-white">{item.name}</div>
              </div>
              <div
                className="text-[9px] font-mono tracking-wider mt-2 uppercase px-1.5 py-0.5 rounded w-fit"
                style={{
                  backgroundColor: `${item.color}20`,
                  color: item.color,
                }}
              >
                {item.badge}
              </div>
            </button>
          );
        })}
      </div>

      {/* Interactive Live Preview Component */}
      <div className="border border-[#1c2738] bg-[#05080e] rounded-lg p-5">
        <div className="text-xs font-mono text-slate-400 mb-3 flex items-center justify-between">
          <span>LIVE INTERACTIVE PREVIEW CARD // RENDERED IN SELECTED SYSTEM:</span>
          <span className="text-[#00f59b] font-bold uppercase">{currentAesthetic}</span>
        </div>

        {/* 1. Industrial Brutalism Preview */}
        {currentAesthetic === 'industrial-brutalism' && (
          <div className="bg-[#0d131f] border border-[#1c2738] rounded-sm p-5 font-mono text-slate-200">
            <div className="flex items-center justify-between border-b border-[#1c2738] pb-2 mb-3">
              <span className="text-[#00f59b] font-bold text-xs tracking-wider flex items-center gap-1.5">
                <span className="w-2 h-2 rounded-full bg-[#00f59b] animate-pulse" />
                TELEMETRY_CONTROLLER // PORT: 8000
              </span>
              <span className="text-[10px] text-slate-400">STATUS: CLOSED_CIRCUIT</span>
            </div>
            <p className="text-xs text-slate-300 mb-4 leading-relaxed font-mono">
              Obsidian canvas (#070a0f) with zero-decoration wireframes. Optimized for high data density,
              command line streaming, and verified RAGAS faithfulness without visual latency.
            </p>
            <div className="flex items-center gap-3">
              <button className="bg-[#00f59b] text-[#070a0f] font-bold px-4 py-2 rounded-sm text-xs uppercase tracking-wider hover:bg-[#00d685] active:translate-y-[1px] transition-transform">
                EXECUTE COMMAND
              </button>
              <span className="border border-[#00f59b]/40 bg-[#00f59b]/10 text-[#00f59b] px-2.5 py-1 rounded-sm text-xs font-mono">
                P95 &lt; 12MS
              </span>
            </div>
          </div>
        )}

        {/* 2. Neo-Brutalism Preview */}
        {currentAesthetic === 'neo-brutalism' && (
          <div className="bg-white border-[3px] border-black rounded-lg shadow-[4px_4px_0px_#000000] p-5 text-black">
            <div className="flex items-center justify-between mb-2">
              <h4 className="font-black text-sm tracking-tight uppercase">SUPERCHARGED VIRAL APP ⚡</h4>
              <span className="bg-[#f43f5e] text-white font-black border-2 border-black px-2 py-0.5 rounded text-[10px] uppercase shadow-[2px_2px_0px_#000000]">
                GEN Z READY
              </span>
            </div>
            <p className="text-xs font-medium text-slate-900 mb-4">
              Thick 3px solid black borders, hard 4px offset drop shadow with ZERO blur, and saturated lemon yellow pop.
              Cuts through generic SaaS monotony on a hackathon projector screen!
            </p>
            <div className="flex items-center gap-3">
              <button className="bg-[#facc15] text-black font-extrabold border-[3px] border-black rounded-lg px-5 py-2.5 shadow-[4px_4px_0px_#000000] hover:shadow-[6px_6px_0px_#000000] hover:-translate-x-[2px] hover:-translate-y-[2px] active:shadow-[1px_1px_0px_#000000] active:translate-x-[3px] active:translate-y-[3px] transition-all text-xs">
                LAUNCH PROJECT 🚀
              </button>
              <span className="bg-[#38bdf8] text-black font-bold border-2 border-black px-3 py-1 rounded text-xs shadow-[2px_2px_0px_#000000]">
                100% DISTINCTIVE
              </span>
            </div>
          </div>
        )}

        {/* 3. Glassmorphism Preview */}
        {currentAesthetic === 'glassmorphism' && (
          <div className="bg-white/[0.05] backdrop-blur-md border border-white/[0.14] rounded-2xl shadow-[0_20px_40px_-15px_rgba(0,0,0,0.5),inset_0_1px_0_rgba(255,255,255,0.2)] p-6 text-slate-100">
            <div className="flex items-center justify-between mb-2">
              <h4 className="font-semibold text-sm tracking-wide text-white">Clinical AI Diagnostic Sheet</h4>
              <span className="bg-sky-500/20 text-sky-300 border border-sky-400/30 px-3 py-1 rounded-full text-[11px] font-medium backdrop-blur-sm">
                HIPAA / SOC 2
              </span>
            </div>
            <p className="text-xs text-slate-300 mb-4 leading-relaxed">
              Multi-tiered translucent frosted glass sheets with specular hairline borders. Projects elite enterprise
              authority, institutional trust, and clinical clarity without visual clutter.
            </p>
            <div className="flex items-center gap-3">
              <button className="bg-sky-500 text-white font-medium px-5 py-2 rounded-xl border border-sky-400/40 shadow-[0_0_20px_rgba(56,189,248,0.3)] hover:scale-[1.02] active:scale-[0.98] transition-transform text-xs">
                Review Patient Analysis
              </button>
              <span className="text-xs text-slate-400 font-mono">Faithfulness: 0.98</span>
            </div>
          </div>
        )}

        {/* 4. Claymorphism Preview */}
        {currentAesthetic === 'claymorphism' && (
          <div className="bg-white rounded-[28px] shadow-[inset_4px_4px_8px_rgba(255,255,255,0.9),inset_-4px_-4px_8px_rgba(165,180,252,0.35),10px_20px_30px_rgba(99,102,241,0.12)] p-6 text-slate-800">
            <div className="flex items-center justify-between mb-2">
              <h4 className="font-bold text-sm text-indigo-950 font-sans">Adaptive Learning Quest 🌟</h4>
              <span className="bg-pink-100 text-pink-700 font-semibold px-3 py-1 rounded-full text-xs shadow-[inset_1px_1px_2px_rgba(255,255,255,0.8)]">
                Level 12 Master
              </span>
            </div>
            <p className="text-xs text-slate-600 mb-4 leading-relaxed font-sans">
              Pillowy soft 3D volumetric surfaces with dual inner inset shadows and friendly pastel hues.
              Lowers cognitive friction and anxiety for students, making daily mastery delightful.
            </p>
            <div className="flex items-center gap-3">
              <button className="bg-indigo-500 text-white rounded-full font-bold px-6 py-2.5 shadow-[inset_2px_2px_4px_rgba(255,255,255,0.8),inset_-2px_-2px_4px_rgba(79,70,229,0.2),6px_12px_20px_rgba(99,102,241,0.25)] hover:scale-[1.03] active:scale-[0.96] transition-transform text-xs">
                Start Today's Quiz
              </button>
              <span className="text-xs text-indigo-500 font-bold">14-Day Streak 🔥</span>
            </div>
          </div>
        )}

        {/* 5. Skeuomorphism Preview */}
        {currentAesthetic === 'skeuomorphism' && (
          <div className="bg-gradient-to-br from-[#252932] to-[#181a20] border border-[#363c4a] rounded-lg shadow-[inset_1px_1px_2px_rgba(255,255,255,0.15),inset_-1px_-1px_3px_rgba(0,0,0,0.8),4px_8px_16px_rgba(0,0,0,0.6)] p-5 text-slate-200">
            <div className="flex items-center justify-between mb-3 border-b border-[#2e333e] pb-2">
              <span className="text-amber-400 font-bold text-xs tracking-wider flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-amber-500 shadow-[0_0_8px_#ff851b]" />
                DSP STUDIO MASTER // VACUUM TUBE TONE
              </span>
              <span className="font-mono text-[10px] text-cyan-400">VU: +3.2 dB</span>
            </div>
            <p className="text-xs text-slate-300 mb-4 leading-relaxed">
              Brushed titanium metal chassis, debossed bezel meters, physical tactile rocker switches, and amber tube warm glows.
              Direct analog muscle-memory mapping for high-precision audio and hardware manipulation.
            </p>
            <div className="flex items-center gap-4">
              <button className="bg-gradient-to-br from-[#2f3542] to-[#1f2229] active:shadow-[inset_2px_2px_5px_rgba(0,0,0,0.9)] border border-[#3c4454] rounded font-semibold text-amber-400 px-5 py-2 text-xs active:translate-y-[1px] transition-transform">
                ENGAGE FILTER
              </button>
              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-[#2f333c] to-[#15171c] shadow-[inset_1px_1px_2px_rgba(255,255,255,0.2),2px_4px_8px_rgba(0,0,0,0.7)] flex items-center justify-center border border-[#363c4a]">
                <div className="w-1.5 h-3 bg-amber-400 rounded-sm" />
              </div>
              <span className="text-xs text-slate-400 font-mono">CUTOFF: 2.4 kHz</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
