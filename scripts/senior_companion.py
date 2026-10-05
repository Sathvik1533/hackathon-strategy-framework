#!/usr/bin/env python3
"""
Senior Orbit: CLI Senior Engineer Companion & Branch Watcher
(scripts/senior_companion.py)

Usage:
  # Instant Senior Guidance for your current branch:
  python3 scripts/senior_companion.py

  # Interactive Teammate Onboarding:
  python3 scripts/senior_companion.py --onboard

  # Ask Senior Orbit a question or code review:
  python3 scripts/senior_companion.py --ask "How do I stream SSE events in FastAPI?"
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

# Ensure root directory is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ai_layer.mascot_agent import HSFMascotAgent, TeammateProfile

PROFILE_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.orbit_profile.json"))


def get_current_git_branch() -> str:
    try:
        res = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            check=True,
        )
        branch = res.stdout.strip()
        return branch if branch else "main"
    except Exception:
        return "main"


def load_local_profile() -> dict:
    if os.path.exists(PROFILE_FILE):
        try:
            with open(PROFILE_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def save_local_profile(profile_dict: dict) -> None:
    try:
        with open(PROFILE_FILE, "w") as f:
            json.dump(profile_dict, f, indent=2)
    except Exception as e:
        print(f"Warning: Could not save .orbit_profile.json: {e}")


def run_onboarding(agent: HSFMascotAgent) -> None:
    print("\n" + "=" * 65)
    print(" 🤝 SENIOR ORBIT: TEAMMATE ONBOARDING WIZARD")
    print("=" * 65)

    current_branch = get_current_git_branch()
    cached = load_local_profile()

    name = input(f"Enter your name [{cached.get('name', 'Developer')}]: ").strip() or cached.get(
        "name", "Developer"
    )

    print("\nSelect your assigned squad role:")
    print("  1) Backend API & Resilience Lead")
    print("  2) Database & Vector Search Lead")
    print("  3) AI & Multi-Agent Architecture Lead")
    print("  4) Frontend Console & Real-Time UX Lead")
    print("  5) Cloud DevOps, CI/CD & Pitch / Demo Lead")

    role_choice = input("Enter choice (1-5) [1]: ").strip() or "1"
    role_map = {
        "1": "Backend API & Resilience Lead",
        "2": "Database & Vector Search Lead",
        "3": "AI & Multi-Agent Architecture Lead",
        "4": "Frontend Console & Real-Time UX Lead",
        "5": "Cloud DevOps, CI/CD & Pitch / Demo Lead",
    }
    role = role_map.get(role_choice, "Backend API & Resilience Lead")

    branch = input(f"Enter your active git branch [{current_branch}]: ").strip() or current_branch

    print("\nSelect your primary Agentic AI IDE:")
    print("  1) Google Antigravity")
    print("  2) Anthropic Claude Code")
    print("  3) Cursor AI")
    print("  4) Windsurf AI")
    print("  5) Hero Agent")
    ide_choice = input("Enter choice (1-5) [1]: ").strip() or "1"
    ide_map = {
        "1": "Google Antigravity",
        "2": "Anthropic Claude Code",
        "3": "Cursor AI",
        "4": "Windsurf AI",
        "5": "Hero Agent",
    }
    ai_ide = ide_map.get(ide_choice, "Google Antigravity")

    goal = (
        input("Enter your contribution goal [Build core features]: ").strip()
        or "Build core features"
    )
    problem = (
        input("Enter hackathon problem statement [Autonomous Enterprise Intelligence]: ").strip()
        or "Autonomous Enterprise Intelligence"
    )

    profile = TeammateProfile(
        name=name,
        role=role,
        contribution_goal=goal,
        knowledge_level="Intermediate",
        ai_ide=ai_ide,
        active_branch=branch,
    )

    save_local_profile(profile.model_dump())
    briefing = agent.onboard_teammate(profile, problem)

    print("\n" + "=" * 65)
    print(f" 👓 {briefing.welcome_message}")
    print("=" * 65)

    print("\n🎯 WHAT YOU MUST DO RIGHT NOW:")
    for do in briefing.senior_guidance.immediate_actions_what_to_do:
        print(f"  ✔ {do}")

    print("\n⚠️ WHAT NOT TO DO (CRITICAL GUARDRAILS):")
    for dont in briefing.senior_guidance.critical_guardrails_what_not_to_do:
        print(f"  {dont}")

    print("\n📋 CUSTOM PROMPT FOR YOUR AI IDE (" + ai_ide + "):")
    print("-" * 65)
    print(briefing.customized_ai_ide_prompt)
    print("-" * 65)
    print(
        "✔ Profile saved to .orbit_profile.json! Run 'hsf pair' anytime to check senior advice.\n"
    )


def print_senior_desk(agent: HSFMascotAgent) -> None:
    current_branch = get_current_git_branch()
    cached = load_local_profile()

    name = cached.get("name", "Developer")
    role = cached.get("role")

    # If role not cached, infer from branch
    if not role:
        if "backend" in current_branch or "api" in current_branch:
            role = "Backend API & Resilience Lead"
        elif "db" in current_branch or "data" in current_branch or "vector" in current_branch:
            role = "Database & Vector Search Lead"
        elif "ai" in current_branch or "agent" in current_branch or "langgraph" in current_branch:
            role = "AI & Multi-Agent Architecture Lead"
        elif "front" in current_branch or "ui" in current_branch or "console" in current_branch:
            role = "Frontend Console & Real-Time UX Lead"
        elif "devops" in current_branch or "cloud" in current_branch or "infra" in current_branch:
            role = "Cloud DevOps, CI/CD & Pitch / Demo Lead"
        else:
            role = "Backend API & Resilience Lead"

    guidance = agent.get_senior_guidance_for_role(role, current_branch)

    print("\n" + "=" * 70)
    print(f" 👓 SENIOR ORBIT: PRINCIPAL ENGINEER DESK (Branch: `{current_branch}`)")
    print("=" * 70)
    print(f"👤 Teammate: {name} | Role: {role}")
    print(f"🎯 Current Mission: {guidance.current_mission}\n")

    print("🎯 WHAT YOU MUST DO RIGHT NOW:")
    for do in guidance.immediate_actions_what_to_do:
        print(f"  ✔ {do}")

    print("\n⚠️ WHAT NOT TO DO (SENIOR GUARDRAILS):")
    for dont in guidance.critical_guardrails_what_not_to_do:
        print(f"  {dont}")

    print(f"\n💡 SENIOR PRO-TIP: {guidance.senior_pro_tip}")
    print("=" * 70 + "\n")


def ask_orbit(agent: HSFMascotAgent, question: str) -> None:
    cached = load_local_profile()
    current_branch = get_current_git_branch()
    role = cached.get("role", "Backend API & Resilience Lead")
    name = cached.get("name", "Developer")

    profile = TeammateProfile(
        name=name,
        role=role,
        contribution_goal=cached.get("contribution_goal", "Deliver features"),
        knowledge_level="Intermediate",
        ai_ide=cached.get("ai_ide", "Antigravity"),
        active_branch=current_branch,
    )

    is_code = any(
        k in question.lower()
        for k in ["select", "from", "import", "def ", "requests", "sleep", "while", "class ", "f'"]
    )
    resp = agent.consult_senior_orbit(profile, question, code_snippet=question if is_code else None)

    print("\n" + "=" * 70)
    print(f' 👓 SENIOR ORBIT ANSWER: "{question}"')
    if resp.groq_powered:
        print(" [⚡ Powered by Groq Llama-3.3-70B]")
    print("=" * 70)
    print(f"\n{resp.advice}\n")
    if resp.code_critique:
        print(f"🔍 CODE REVIEW CRITIQUE:\n{resp.code_critique}\n")
    print("=" * 70 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Senior Orbit CLI Companion")
    parser.add_argument(
        "--onboard", action="store_true", help="Launch interactive teammate onboarding wizard"
    )
    parser.add_argument(
        "--ask", type=str, help="Ask Senior Orbit a question or request a code review"
    )
    args = parser.parse_args()

    agent = HSFMascotAgent()

    if args.onboard:
        run_onboarding(agent)
    elif args.ask:
        ask_orbit(agent, args.ask)
    else:
        print_senior_desk(agent)


if __name__ == "__main__":
    main()
