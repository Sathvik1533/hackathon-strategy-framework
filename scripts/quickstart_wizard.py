#!/usr/bin/env python3
"""
Interactive Quickstart Wizard for Hackathon Strategy Framework (HSF).
Enables any teammate to onboard in under 60 seconds, choose their role,
receive their companion Autobot, checkout their git branch, and generate their
custom AI IDE prompt with zero friction.
"""

import argparse
import json
import subprocess
from pathlib import Path

# Color and style helpers
CYAN = "\033[1;36m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
BLUE = "\033[1;34m"
PURPLE = "\033[1;35m"
RED = "\033[1;31m"
BOLD = "\033[1m"
RESET = "\033[0m"

ROLES_MAP = {
    "1": {
        "key": "frontend",
        "title": "Frontend & Real-Time UX Lead",
        "robot": "Mirage 🎨✨ (Frontend Hologram Specialist)",
        "layers": ["Frontend UI", "Aesthetic Design Tokens", "Client State (SSE)"],
        "branch": "feat/frontend-views",
        "files_to_edit": [
            "frontend/index.html (or mascot-dashboard/src/app/page.tsx)",
            "frontend/style.css (Design tokens & theme)",
            "frontend/app.js (SSE event stream integration)",
        ],
        "core_commands": [
            "open frontend/index.html (or cd mascot-dashboard && npm run dev)",
            "npx hsf aesthetic (to inspect design tokens)",
        ],
        "do_not_touch": ["backend/src/app/core/redis.py", "database/supabase_rls.sql"],
    },
    "2": {
        "key": "backend",
        "title": "Backend API & Resilience Lead",
        "robot": "Ironhide 🛡️⚡ (Backend Titan & Resilience Sentinel)",
        "layers": ["FastAPI Routes", "Redis Pool & Rate Limiter", "Circuit Breakers"],
        "branch": "feat/backend-api",
        "files_to_edit": [
            "backend/src/app/api/v1/endpoints/ (Domain routes)",
            "backend/src/app/core/redis.py (Caching & Rate limits)",
            "backend/tests/test_api.py (Unit & Integration tests)",
        ],
        "core_commands": [
            "PYTHONPATH=backend pytest (Run 17 test suite)",
            "curl http://localhost:8000/api/v1/health (Verify API)",
        ],
        "do_not_touch": ["frontend/index.html", "pitch/pitch.marp.md"],
    },
    "3": {
        "key": "ai",
        "title": "AI Systems & Multi-Agent Lead",
        "robot": "Wheeljack 🔬⚡ (AI & Multi-Agent Weaponsmith)",
        "layers": ["LangGraph StateGraph", "FastMCP SSE Server", "FlashRank Reranker"],
        "branch": "feat/ai-multi-agent",
        "files_to_edit": [
            "ai_layer/langgraph_supervisor.py (Agent state machine)",
            "ai_layer/fastmcp_server.py (SSE tool server on port 8001)",
            "ai_layer/flashrank_reranker.py (Neural cross-encoder)",
        ],
        "core_commands": [
            "python3 ai_layer/langgraph_supervisor.py (Test agent loop)",
            "python3 ai_layer/eval_harness.py (Run RAGAS accuracy eval)",
        ],
        "do_not_touch": ["infra/docker-compose.yml", "frontend/style.css"],
    },
    "4": {
        "key": "database",
        "title": "Database & pgvector Lead",
        "robot": "Ratchet 🏥💾 (Database & Security Guardian)",
        "layers": ["PostgreSQL 16", "pgvector HNSW Index", "Supabase RLS Policies"],
        "branch": "feat/database-vector",
        "files_to_edit": [
            "database/seed_data.py (Seed records & synthetic vectors)",
            "database/supabase_rls.sql (Row-Level Security rules)",
            "ai_layer/hybrid_retriever.py (Dense HNSW + Sparse BM25)",
        ],
        "core_commands": [
            "python3 database/seed_data.py (Re-seed vector database)",
            "docker compose -f infra/docker-compose.yml exec db psql -U postgres (Inspect SQL)",
        ],
        "do_not_touch": ["frontend/index.html", "pitch/demo.sh"],
    },
    "5": {
        "key": "devops_pitch",
        "title": "Cloud DevOps & Live Pitch Lead",
        "robot": "Bumblebee 🐝🚀 (Cloud DevOps & Stage Scout)",
        "layers": ["Docker Multi-Stage", "AWS ECS Fargate", "Marp Pitch Deck & demo.sh"],
        "branch": "feat/devops-pitch",
        "files_to_edit": [
            "pitch/pitch.marp.md (6-minute presentation slides)",
            "pitch/demo.sh (30-second offline terminal demo script)",
            "infra/Dockerfile & infra/aws-architecture.md",
        ],
        "core_commands": [
            "npx hsf pitch (Compile Marp deck to HTML)",
            "bash pitch/demo.sh (Execute live stage demo backup)",
        ],
        "do_not_touch": ["backend/src/app/core/", "ai_layer/hybrid_retriever.py"],
    },
    "6": {
        "key": "qa_eval",
        "title": "QA, Benchmarks & Evaluation Specialist",
        "robot": "Orbit Prime 🤖⭐ (Supreme Autobot Commander)",
        "layers": ["RAGAS Evaluation", "Latency Benchmarking", "Security Guardrails"],
        "branch": "feat/qa-eval-benchmarks",
        "files_to_edit": [
            "ai_layer/eval_harness.py (25-case golden dataset)",
            "ai_layer/guardrails.py (Input injection defense)",
            "backend/tests/test_api.py (Coverage expansion)",
        ],
        "core_commands": [
            "python3 ai_layer/eval_harness.py (Execute golden eval suite)",
            "python3 scripts/generate_judge_report.py (Generate judge certificate)",
        ],
        "do_not_touch": ["frontend/index.html", "pitch/pitch.marp.md"],
    },
}


def print_banner():
    print(
        f"""{CYAN}
╔═══════════════════════════════════════════════════════════════════════════════╗
║          🚀 HACKATHON STRATEGY FRAMEWORK (HSF) QUICKSTART WIZARD             ║
║            Zero-Friction Onboarding for Full-Stack & Agentic AI Squads        ║
╚═══════════════════════════════════════════════════════════════════════════════╝{RESET}"""
    )


def check_prerequisites():
    print(f"\n{YELLOW}🔍 [Step 1/5] Checking System Prerequisites...{RESET}")
    tools = [
        ("python3", "Python 3.11+", True),
        ("docker", "Docker Engine", False),
        ("node", "Node.js (for CLI & Next.js)", False),
        ("git", "Git Version Control", True),
    ]
    all_good = True
    for cmd, name, required in tools:
        found = subprocess.run(f"command -v {cmd}", shell=True, capture_output=True).returncode == 0
        if found:
            print(f"  {GREEN}✔ {name} is installed.{RESET}")
        else:
            if required:
                print(f"  {RED}❌ {name} ({cmd}) is missing! Required for HSF.{RESET}")
                all_good = False
            else:
                print(f"  {YELLOW}⚠️  {name} ({cmd}) not detected globally (Optional for local mocks).{RESET}")
    return all_good


def prompt_user_profile(auto=False, default_role="2"):
    print(f"\n{YELLOW}👤 [Step 2/5] Teammate Profile & Problem Statement Setup...{RESET}")

    if auto:
        problem = "Autonomous Enterprise Multi-Agent Intelligence System"
        team_size = 5
        name = "Teammate"
        role_choice = default_role
    else:
        # Problem statement
        prompt_prob = f"{BOLD}Enter your Hackathon Problem Statement{RESET} [Press Enter for default]: "
        problem_input = input(prompt_prob).strip()
        problem = problem_input if problem_input else "Autonomous Enterprise Multi-Agent Intelligence System"

        # Team size
        prompt_size = f"{BOLD}How many members are in your squad?{RESET} [1-6, default: 5]: "
        size_input = input(prompt_size).strip()
        try:
            team_size = int(size_input) if size_input else 5
        except ValueError:
            team_size = 5

        # Name
        prompt_name = f"{BOLD}What is your name / GitHub handle?{RESET} [default: Developer]: "
        name_input = input(prompt_name).strip()
        name = name_input if name_input else "Developer"

        # Role selection
        print(f"\n{CYAN}Select your primary role for this sprint:{RESET}")
        for k, v in ROLES_MAP.items():
            print(f"  {BOLD}[{k}]{RESET} {v['title']} (Companion: {v['robot']})")

        role_choice = input(f"\n{BOLD}Choose role [1-6, default: 2 (Backend)]: {RESET}").strip()
        if role_choice not in ROLES_MAP:
            role_choice = "2"

    selected_role = ROLES_MAP[role_choice]
    print(f"\n{GREEN}✔ Profile confirmed:{RESET} {name} as {BOLD}{selected_role['title']}{RESET}")
    print(f"✔ Companion Autobot: {selected_role['robot']}")
    return problem, team_size, name, selected_role


def setup_git_branch(branch_name):
    print(f"\n{YELLOW}🌿 [Step 3/5] Setting Up Isolated Git Branch...{RESET}")
    try:
        # Check current branch
        curr = subprocess.run("git rev-parse --abbrev-ref HEAD", shell=True, capture_output=True, text=True).stdout.strip()
        if curr == branch_name:
            print(f"  {GREEN}✔ Already on branch {branch_name}{RESET}")
        else:
            # Check if branch exists
            check = subprocess.run(f"git show-ref --verify --quiet refs/heads/{branch_name}", shell=True).returncode
            if check == 0:
                subprocess.run(f"git checkout {branch_name}", shell=True, check=True)
                print(f"  {GREEN}✔ Switched to existing branch: {branch_name}{RESET}")
            else:
                subprocess.run(f"git checkout -b {branch_name}", shell=True, check=True)
                print(f"  {GREEN}✔ Created and checked out new branch: {branch_name}{RESET}")
    except Exception as e:
        print(f"  {YELLOW}ℹ Git branch setup skipped or manual: {e}{RESET}")


def generate_teammate_prompt_and_memory(problem, team_size, name, role_info):
    print(f"\n{YELLOW}📝 [Step 4/5] Generating Personalized AI IDE Prompt & Telemetry...{RESET}")
    hsf_dir = Path(".hsf")
    hsf_dir.mkdir(exist_ok=True)

    # 1. Generate customized AI prompt markdown
    prompt_file = hsf_dir / "my_agent_prompt.md"
    prompt_content = f"""# 🤖 Hackathon Agent Prompt: {role_info['title']}
**Teammate**: {name}  
**Companion Autobot**: {role_info['robot']}  
**Sprint Problem Statement**: "{problem}"  
**Assigned Git Branch**: `{role_info['branch']}`  
**Assigned Layers**: {', '.join(role_info['layers'])}  

---

## 🎯 Your Mission & Architectural Contract
You are paired with **{role_info['robot']}** in the Hackathon Strategy Framework (HSF).
Your job is to implement production-grade, tested solutions for:
**{problem}**

### 📁 Your Primary Files to Edit:
{chr(10).join(['- `' + f + '`' for f in role_info['files_to_edit']])}

### 🚫 DO NOT TOUCH (Zero-Collision Rule):
{chr(10).join(['- `' + f + '`' for f in role_info['do_not_touch']])}

### ⚡ Verification Commands:
{chr(10).join(['```bash', *role_info['core_commands'], '```'])}

---

## 🧠 Instructions for Your AI IDE (Cursor / Claude Code / Antigravity):
Copy and paste this prompt to your AI assistant:
> "I am {name}, acting as {role_info['title']} paired with {role_info['robot']} on branch `{role_info['branch']}`.
> We are solving: '{problem}'.
> Strictly respect the zero-collision boundaries. Touch only my assigned files.
> Implement production patterns with full error handling, Pydantic type safety, and unit tests."
"""
    prompt_file.write_text(prompt_content, encoding="utf-8")
    print(f"  {GREEN}✔ Generated IDE prompt:{RESET} .hsf/my_agent_prompt.md")

    # 2. Update telemetry in .hsf/memory.json
    mem_file = hsf_dir / "memory.json"
    memory_data = {
        "version": "1.0",
        "last_updated": "2026-10-05T23:00:00Z",
        "team_size": team_size,
        "problem_statement": problem,
        "teammates_tracked": {},
    }
    if mem_file.exists():
        try:
            memory_data = json.loads(mem_file.read_text(encoding="utf-8"))
        except Exception:
            pass

    if "teammates_tracked" not in memory_data:
        memory_data["teammates_tracked"] = {}

    memory_data["teammates_tracked"][name.lower()] = {
        "name": name,
        "role": role_info["title"],
        "branch": role_info["branch"],
        "companion": role_info["robot"],
        "onboarded_at": "2026-10-05T23:00:00Z",
    }
    mem_file.write_text(json.dumps(memory_data, indent=2), encoding="utf-8")
    print(f"  {GREEN}✔ Saved Senior Orbit memory state:{RESET} .hsf/memory.json")


def print_completion_summary(name, role_info):
    print(f"\n{GREEN}==============================================================================={RESET}")
    print(f"{GREEN}🎉 ONBOARDING COMPLETE! YOU ARE READY TO SPRINT IN 60 SECONDS!{RESET}")
    print(f"{GREEN}==============================================================================={RESET}")
    print(f"\n{BOLD}Teammate:{RESET}  {name}")
    print(f"{BOLD}Role:{RESET}      {role_info['title']}")
    print(f"{BOLD}Companion:{RESET} {role_info['robot']}")
    print(f"{BOLD}Branch:{RESET}    {CYAN}{role_info['branch']}{RESET}")
    print(f"\n{BOLD}📂 Your 3 Files to Edit:{RESET}")
    for f in role_info["files_to_edit"]:
        print(f"   • {CYAN}{f}{RESET}")

    print(f"\n{BOLD}⚡ Your 2 Core Commands:{RESET}")
    for c in role_info["core_commands"]:
        print(f"   $ {YELLOW}{c}{RESET}")

    print(f"\n{BOLD}🤖 What to do next:{RESET}")
    print(f"   1. Open {CYAN}.hsf/my_agent_prompt.md{RESET} and paste it into your AI IDE (Antigravity/Cursor/Claude).")
    print(f"   2. Start developing your feature in branch {CYAN}{role_info['branch']}{RESET}.")
    print(f"   3. Need advice? Ask Senior Orbit: {YELLOW}python3 scripts/senior_companion.py --ask \"How do I build this?\"{RESET}")
    print(f"{GREEN}==============================================================================={RESET}\n")


def main():
    parser = argparse.ArgumentParser(description="HSF Teammate Quickstart Onboarding Wizard")
    parser.add_argument("--auto", action="store_true", help="Run in non-interactive automatic mode")
    parser.add_argument("--role", default="2", choices=list(ROLES_MAP.keys()), help="Default role choice (1-6)")
    args = parser.parse_args()

    print_banner()
    check_prerequisites()
    problem, team_size, name, role_info = prompt_user_profile(auto=args.auto, default_role=args.role)
    setup_git_branch(role_info["branch"])
    generate_teammate_prompt_and_memory(problem, team_size, name, role_info)
    print_completion_summary(name, role_info)


if __name__ == "__main__":
    main()
