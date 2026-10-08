#!/usr/bin/env python3
"""
CLI Dynamic Multi-Agent Mentoring Orchestrator for HSF.
Allows developers and teammates to receive real-time, role-adaptive mentoring
from Autobot companions, architecture supervisors, and peer synergy coordinators.
"""

import argparse
import sys
from pathlib import Path

# Ensure repo root is on path
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ai_layer.mentor_orchestrator import (  # noqa: E402
    MentoringConsultationRequest,
    MultiAgentMentorOrchestrator,
)

CYAN = "\033[1;36m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
PURPLE = "\033[1;35m"
BLUE = "\033[1;34m"
RED = "\033[1;31m"
DIM = "\033[90m"
BOLD = "\033[1m"
RESET = "\033[0m"


def main():
    parser = argparse.ArgumentParser(description="HSF Dynamic Multi-Agent Mentoring Orchestrator")
    parser.add_argument(
        "--role",
        "-r",
        default="Backend Lead",
        help="Your role (Lead Architect, Backend Lead, DevOps Lead, AI Lead, Frontend Lead)",
    )
    parser.add_argument("--teammate", "-t", default="Teammate", help="Your name")
    parser.add_argument(
        "--stage",
        "-s",
        default="hour_0",
        choices=["hour_0", "hour_4", "hour_12", "hour_18", "hour_22", "hour_24"],
        help="Hackathon stage",
    )
    parser.add_argument(
        "--problem",
        "-p",
        default="Real-Time Autonomous Agentic Platform",
        help="Hackathon problem statement",
    )
    parser.add_argument(
        "--blocker", "-b", default=None, help="Optional current blocker or challenge"
    )

    args = parser.parse_args()

    req = MentoringConsultationRequest(
        teammate_name=args.teammate,
        role=args.role,
        stage=args.stage,
        problem_statement=args.problem,
        current_blocker=args.blocker,
    )

    session = MultiAgentMentorOrchestrator.orchestrate(req)

    print(
        f"\n{CYAN}╔═══════════════════════════════════════════════════════════════════════════════╗{RESET}"
    )
    print(
        f"{CYAN}║     🤖 HSF DYNAMIC MULTI-AGENT MENTORING ORCHESTRATION COCKPIT                ║{RESET}"
    )
    print(
        f"{CYAN}╚═══════════════════════════════════════════════════════════════════════════════╝{RESET}\n"
    )

    print(
        f"👤 {BOLD}Teammate:{RESET} {GREEN}{session.teammate_name}{RESET}  |  🎯 {BOLD}Role:{RESET} {YELLOW}{session.role}{RESET}"
    )
    print(
        f"🤖 {BOLD}Autobot Companion:{RESET} {PURPLE}{session.companion.autobot}{RESET} ({session.companion.title})"
    )
    print(f"⚡ {BOLD}Superpower:{RESET} {DIM}{session.companion.superpower}{RESET}")
    print(
        f"⏱️  {BOLD}Hackathon Milestone:{RESET} {CYAN}{session.current_stage.name} ({session.current_stage.hour}){RESET}"
    )
    print(f"🎯 {BOLD}Challenge Focus:{RESET} {BOLD}{session.problem_statement}{RESET}\n")

    # 1. Autobot Persona Advice
    print(
        f"{PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}"
    )
    print(f"🛡️  {BOLD}[AUTOBOT COPILOT]: {session.persona_advice.agent_name}{RESET}")
    print(
        f"{PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}"
    )
    print(f"{session.persona_advice.advice}\n")
    print(f"{BOLD}Key Tactical Action Items:{RESET}")
    for item in session.persona_advice.action_items:
        print(f"  {GREEN}✔{RESET} {item}")

    # 2. Architecture Supervisor
    print(
        f"\n{BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}"
    )
    print(f"🏛️  {BOLD}[SYSTEM SUPERVISOR]: {session.architecture_supervisor.agent_name}{RESET}")
    print(
        f"{BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}"
    )
    print(f"{session.architecture_supervisor.advice}\n")
    for item in session.architecture_supervisor.action_items:
        print(f"  {BLUE}⚡{RESET} {item}")

    # 3. Peer Synergy Coordinator
    print(
        f"\n{YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}"
    )
    print(f"🤝  {BOLD}[PEER SYNERGY COORDINATOR]: {session.peer_synergy_agent.agent_name}{RESET}")
    print(
        f"{YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}"
    )
    print(f"{session.peer_synergy_agent.advice}\n")
    for item in session.peer_synergy_agent.action_items:
        print(f"  {YELLOW}🤝{RESET} {item}")

    # 4. Immediate Commands & Bounty
    print(
        f"\n{GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}"
    )
    print(f"🚀  {BOLD}[ACTION DISPATCHER]: Immediate Stage Commands & XP Bounty{RESET}")
    print(
        f"{GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}"
    )
    for cmd in session.recommended_commands:
        print(f"  {CYAN}$ {cmd}{RESET}")
    print(
        f"\n🎁 {BOLD}Available Bounty:{RESET} {YELLOW}+{session.xp_bounty_available} XP{RESET} (Quest ID: {CYAN}{session.quest_id}{RESET})"
    )
    print(
        f'   Claim command: {DIM}npx hsf quest claim {session.quest_id} --teammate "{session.teammate_name}"{RESET}\n'
    )


if __name__ == "__main__":
    main()
