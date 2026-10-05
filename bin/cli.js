#!/usr/bin/env node

/**
 * Hackathon Strategy Framework (HSF) CLI
 * Accelerated bootstrapping for Agentic AI & Full-Stack Hackathon Projects
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const command = process.argv[2] || 'help';

function banner() {
  console.log(`
\x1b[36m╔════════════════════════════════════════════════════════════════════╗
║             🚀 HACKATHON STRATEGY FRAMEWORK (HSF) v1.0             ║
║  Zero-To-Production Agentic Stack (FastAPI + LangGraph + pgvector) ║
╚════════════════════════════════════════════════════════════════════╝\x1b[0m
`);
}

function run(cmd, desc) {
  console.log(`\x1b[33m⚡ ${desc}...\x1b[0m`);
  try {
    execSync(cmd, { stdio: 'inherit' });
  } catch (error) {
    console.error(`\x1b[31m❌ Failed: ${desc}\x1b[0m`);
    process.exit(1);
  }
}

switch (command) {
  case 'init':
    banner();
    console.log(`\x1b[32m[Step 1/4] Checking Environment & Setting up .env\x1b[0m`);
    if (!fs.existsSync('.env')) {
      if (fs.existsSync('.env.example')) {
        fs.copyFileSync('.env.example', '.env');
        console.log(`✔ Created .env from .env.example`);
      }
    } else {
      console.log(`✔ .env already exists`);
    }

    console.log(`\x1b[32m[Step 2/4] Verifying Core Engines\x1b[0m`);
    run('python3 --version', 'Checking Python');
    run('docker --version', 'Checking Docker');

    console.log(`\x1b[32m[Step 3/4] Launching Isolated Multi-Service Container Stack\x1b[0m`);
    run('docker compose -f infra/docker-compose.yml up -d', 'Starting Docker Containers');

    console.log(`\x1b[32m[Step 4/4] Seeding Vector Database\x1b[0m`);
    setTimeout(() => {
      try {
        run('docker compose -f infra/docker-compose.yml exec -T api python database/seed_data.py', 'Seeding Postgres + pgvector');
      } catch (e) {
        console.log('ℹ Seeding will run once DB container completes startup.');
      }
      console.log(`
\x1b[32m🎉 Hackathon Stack Online!\x1b[0m
• API & Swagger Docs: \x1b[34mhttp://localhost:8000/docs\x1b[0m
• Health Endpoint:    \x1b[34mhttp://localhost:8000/api/v1/health\x1b[0m
• Frontend Dashboard: \x1b[34mhttp://localhost:8000\x1b[0m (or open frontend/index.html)
• FastMCP SSE Tool:   \x1b[34mhttp://localhost:8001/sse\x1b[0m
• Pitch Deck:         Run \x1b[33mnpx hsf pitch\x1b[0m to generate pitch deck HTML
      `);
    }, 4000);
    break;

  case 'pitch':
    banner();
    run('marp pitch/pitch.marp.md -o pitch/presentation.html', 'Generating HTML Presentation');
    try {
      run('marp --pdf pitch/pitch.marp.md -o pitch/pitch_deck.pdf', 'Generating PDF Presentation');
    } catch (e) {
      console.log('ℹ PDF export requires Chrome/Chromium; HTML presentation generated successfully.');
    }
    console.log(`\x1b[32m✔ Pitch Deck Ready: pitch/presentation.html\x1b[0m`);
    break;

  case 'demo':
    banner();
    run('bash pitch/demo.sh', 'Running Live Stage Terminal Demo');
    break;

  case 'eval':
    banner();
    run('python3 ai_layer/eval_harness.py', 'Running RAGAS & Grounding Eval Suite');
    break;

  case 'review':
    banner();
    run('python3 scripts/review_pr.py', 'Running Automated PR Reviewer Agent');
    break;

  case 'diagram':
  case 'archify':
    banner();
    console.log(`\x1b[32m✔ Building Interactive Archify Architecture Diagram\x1b[0m`);
    {
      const archifyPath = fs.existsSync('/Users/k.sathvik/.gemini/config/skills/archify/bin/archify.mjs')
        ? '/Users/k.sathvik/.gemini/config/skills/archify/bin/archify.mjs'
        : 'archify';
      run(`node ${archifyPath} deliver architecture .archify/architecture-fullstack-topology-20261005-070500/candidate.json docs/architecture/system-architecture.html --repo-root . --quality showcase --json`, 'Generating Archify Diagram');
      console.log(`
\x1b[32m✔ Interactive Archify Architecture Diagram Ready!\x1b[0m
• Interactive HTML View: \x1b[34mdocs/architecture/system-architecture.html\x1b[0m
• Inspect in Browser:    \x1b[33mopen docs/architecture/system-architecture.html\x1b[0m
      `);
    }
    break;

  case 'strategize':
    banner();
    {
      const problem = process.argv.slice(3).join(' ') || 'Autonomous Enterprise Multi-Agent Intelligence System';
      console.log(`\x1b[36m🤖 Orbit Mascot Agent analyzing: "${problem}"...\x1b[0m\n`);
      run(`python3 scripts/mascot_agent.py "${problem.replace(/"/g, '\\"')}"`, 'Executing Orbit Mascot Strategizer');
    }
    break;

  case 'help':
  default:
    banner();
    console.log(`
\x1b[1mAvailable Commands:\x1b[0m
  \x1b[33mhsf init\x1b[0m        - Bootstrap .env, launch Docker multi-service stack, and seed DB
  \x1b[33mhsf strategize\x1b[0m  - Activate Orbit Mascot Agent to deconstruct problem & generate prompts
  \x1b[33mhsf pitch\x1b[0m       - Compile Marp Markdown into interactive HTML/PDF pitch slides
  \x1b[33mhsf demo\x1b[0m        - Run animated terminal cURL demo (stage backup if UI lags)
  \x1b[33mhsf eval\x1b[0m        - Run RAGAS 25-case golden dataset accuracy & faithfulness tests
  \x1b[33mhsf review\x1b[0m      - Run automated PR reviewer agent on latest branch changes
  \x1b[33mhsf diagram\x1b[0m     - Deliver verified Archify full-stack architecture diagram HTML

\x1b[1mQuickstart for Teammates:\x1b[0m
  1. git clone https://github.com/Sathvik1533/hackathon-strategy-framework.git
  2. cd hackathon-strategy-framework
  3. ./init.sh
  4. hsf strategize "Your Hackathon Problem Statement"
    `);
    break;
}
