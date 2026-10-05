'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Cpu, ShieldCheck, Zap, Radio, Terminal } from 'lucide-react';

interface RoboticMascotProps {
  statusText?: string;
  activeRole?: string;
  telemetryMode?: 'NOMINAL' | 'ANALYZING' | 'ALERT' | 'GUARDRAIL';
}

export const RoboticMascotChassis: React.FC<RoboticMascotProps> = ({
  statusText = 'SYSTEMS NOMINAL // WATCHING ACTIVE BRANCH',
  activeRole = 'Senior Principal Robotic Director',
  telemetryMode = 'NOMINAL',
}) => {
  const [antennaFrequency, setAntennaFrequency] = useState(144.8);
  const [servoAngle, setServoAngle] = useState(0);

  const getLedColor = () => {
    switch (telemetryMode) {
      case 'ALERT':
        return '#ef4444';
      case 'GUARDRAIL':
        return '#f59e0b';
      case 'ANALYZING':
        return '#00b4d8';
      default:
        return '#00f59b';
    }
  };

  return (
    <div className="relative bg-[#0d131f] border border-[#1c2738] rounded-lg p-6 shadow-2xl flex flex-col items-center justify-center overflow-hidden">
      {/* Background HUD Grid & Coordinate Labels */}
      <div className="absolute inset-0 hud-scanline opacity-40 pointer-events-none" />
      <div className="absolute top-2 left-3 text-[10px] font-mono text-[#00b4d8]/60 tracking-wider">
        SYS.REV // ORBIT-MK4-ROBOTIC
      </div>
      <div className="absolute top-2 right-3 text-[10px] font-mono text-[#00f59b]/80 flex items-center gap-1.5">
        <span
          className="w-2 h-2 rounded-full animate-ping"
          style={{ backgroundColor: getLedColor() }}
        />
        {telemetryMode}
      </div>

      {/* SVG Mechanical Robotic Body */}
      <motion.div
        className="relative my-4 cursor-pointer"
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
        animate={{ y: [0, -3, 0] }}
        transition={{
          duration: 3,
          repeat: Infinity,
          ease: [0.16, 1, 0.3, 1], // Emil Kowalski / Hallmark ease-out
        }}
        onClick={() => setServoAngle((prev) => (prev === 0 ? 5 : prev === 5 ? -5 : 0))}
      >
        <svg
          width="200"
          height="200"
          viewBox="0 0 200 200"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          className="drop-shadow-[0_10px_25px_rgba(0,0,0,0.8)]"
        >
          {/* External Antenna with Signal Waves */}
          <path d="M100 25 L100 8" stroke="#334155" strokeWidth="3" strokeLinecap="round" />
          <circle cx="100" cy="8" r="4" fill={getLedColor()} className="animate-pulse" />
          <path
            d="M92 4 C95 1, 105 1, 108 4"
            stroke={getLedColor()}
            strokeWidth="1.5"
            strokeLinecap="round"
            opacity="0.6"
          />

          {/* Neck Hydraulic Piston Mount */}
          <rect x="88" y="148" width="24" height="20" rx="3" fill="#1e293b" stroke="#334155" strokeWidth="1.5" />
          <line x1="94" y1="150" x2="94" y2="166" stroke="#475569" strokeWidth="2" />
          <line x1="106" y1="150" x2="106" y2="166" stroke="#475569" strokeWidth="2" />

          {/* Main Robotic Head Chassis (Titanium Hex Plate) */}
          <path
            d="M45 45 L155 45 L170 85 L160 145 L40 145 L30 85 Z"
            fill="url(#titaniumChassis)"
            stroke="#334155"
            strokeWidth="2"
          />

          {/* Bolt Rivets on Corners */}
          <circle cx="48" cy="52" r="2.5" fill="#475569" stroke="#1e293b" strokeWidth="0.5" />
          <circle cx="152" cy="52" r="2.5" fill="#475569" stroke="#1e293b" strokeWidth="0.5" />
          <circle cx="45" cy="138" r="2.5" fill="#475569" stroke="#1e293b" strokeWidth="0.5" />
          <circle cx="155" cy="138" r="2.5" fill="#475569" stroke="#1e293b" strokeWidth="0.5" />

          {/* Heatsink Cooling Vents (Top) */}
          <line x1="70" y1="52" x2="130" y2="52" stroke="#1e293b" strokeWidth="2.5" strokeLinecap="round" />
          <line x1="74" y1="58" x2="126" y2="58" stroke="#1e293b" strokeWidth="2.5" strokeLinecap="round" />

          {/* Mechanical Optical Visor Housing */}
          <rect
            x="48"
            y="72"
            width="104"
            height="44"
            rx="6"
            fill="#05070a"
            stroke="#1e293b"
            strokeWidth="2"
          />

          {/* Optical Visor Glass Layer */}
          <rect
            x="52"
            y="76"
            width="96"
            height="36"
            rx="4"
            fill="#0b1320"
            stroke={getLedColor()}
            strokeWidth="0.8"
            strokeOpacity="0.4"
          />

          {/* Dual Cybernetic Optical Sensors (Eyes) */}
          <g>
            {/* Left Eye: High-Precision Target Lens */}
            <circle cx="78" cy="94" r="12" fill="#0f172a" stroke="#334155" strokeWidth="1.5" />
            <circle cx="78" cy="94" r="7" fill={getLedColor()} fillOpacity="0.3" stroke={getLedColor()} strokeWidth="1" />
            <circle cx="78" cy="94" r="3" fill={getLedColor()} />
            <circle cx="76" cy="92" r="1.5" fill="#ffffff" />

            {/* Right Eye: High-Precision Target Lens */}
            <circle cx="122" cy="94" r="12" fill="#0f172a" stroke="#334155" strokeWidth="1.5" />
            <circle cx="122" cy="94" r="7" fill={getLedColor()} fillOpacity="0.3" stroke={getLedColor()} strokeWidth="1" />
            <circle cx="122" cy="94" r="3" fill={getLedColor()} />
            <circle cx="120" cy="92" r="1.5" fill="#ffffff" />
          </g>

          {/* Scanning Laser Beam across Visor */}
          <motion.line
            x1="54"
            y1="94"
            x2="146"
            y2="94"
            stroke={getLedColor()}
            strokeWidth="1.5"
            strokeLinecap="round"
            opacity="0.8"
            animate={{ y1: [78, 110, 78], y2: [78, 110, 78] }}
            transition={{ duration: 2.2, repeat: Infinity, ease: 'linear' }}
          />

          {/* Speaker / Vocoder Mesh (Mouth Grille) */}
          <g opacity="0.7">
            <line x1="82" y1="126" x2="118" y2="126" stroke="#475569" strokeWidth="2" strokeDasharray="3 3" />
            <line x1="86" y1="132" x2="114" y2="132" stroke="#475569" strokeWidth="2" strokeDasharray="3 3" />
          </g>

          {/* Titanium Shading Gradients */}
          <defs>
            <linearGradient id="titaniumChassis" x1="45" y1="45" x2="160" y2="145" gradientUnits="userSpaceOnUse">
              <stop offset="0%" stopColor="#242b38" />
              <stop offset="50%" stopColor="#1a202c" />
              <stop offset="100%" stopColor="#0f141d" />
            </linearGradient>
          </defs>
        </svg>
      </motion.div>

      {/* Live Robotic Telemetry Status Bar */}
      <div className="w-full bg-[#05080e] border border-[#1c2738] rounded p-3 mt-2 font-mono text-xs text-slate-300">
        <div className="flex items-center justify-between border-b border-[#1c2738]/60 pb-2 mb-2">
          <span className="text-[#00f59b] font-bold flex items-center gap-1.5">
            <Cpu className="w-3.5 h-3.5" /> ORBIT STATUS
          </span>
          <span className="text-[#00b4d8] text-[11px]">FREQ: {antennaFrequency} MHz</span>
        </div>
        <p className="text-slate-400 text-[11px] leading-relaxed mb-2 font-mono">
          &gt; <span className="text-[#00f59b]">{statusText}</span>
        </p>

        {/* Real-Time Hardware Dials / Metrics */}
        <div className="grid grid-cols-3 gap-2 text-[10px] text-slate-400 pt-1">
          <div className="bg-[#0b101b] p-1.5 rounded border border-[#141b27]">
            <div className="text-slate-500">SERVO ANGLE</div>
            <div className="text-white font-bold">{servoAngle}° (CALIBRATED)</div>
          </div>
          <div className="bg-[#0b101b] p-1.5 rounded border border-[#141b27]">
            <div className="text-slate-500">LATENCY P95</div>
            <div className="text-[#00f59b] font-bold">8.4 ms (CACHED)</div>
          </div>
          <div className="bg-[#0b101b] p-1.5 rounded border border-[#141b27]">
            <div className="text-slate-500">FAITHFULNESS</div>
            <div className="text-[#00b4d8] font-bold">0.96 (RAGAS)</div>
          </div>
        </div>
      </div>
    </div>
  );
};
