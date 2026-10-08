#!/usr/bin/env python3
"""
CLI Leaderboard & Teammate Arena Runner for HSF.
Displays rich terminal scoreboard, quests catalog, claim actions, and cheers.
"""

import argparse
import sys
from pathlib import Path

# Ensure repo root is on path
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ai_layer.gamification_engine import GamificationEngine  # noqa: E402

CYAN = "\033[1;36m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
PURPLE = "\033[1;35m"
BLUE = "\033[1;34m"
DIM = "\033[90m"
BOLD = "\033[1m"
RESET = "\033[0m"


def show_leaderboard():
    engine = GamificationEngine()
    board = engine.get_leaderboard()

    print(
        f"\n{CYAN}╔═══════════════════════════════════════════════════════════════════════════════╗{RESET}"
    )
    print(
        f"{CYAN}║             🎮 HSF CYBERNETIC ARENA • TEAMMATE LEADERBOARD                    ║{RESET}"
    )
    print(
        f"{CYAN}╚═══════════════════════════════════════════════════════════════════════════════╝{RESET}\n"
    )

    print(
        f"{YELLOW}🏆 Team: {board['team_name']}{RESET}  |  "
        f"{GREEN}⭐ Total XP: {board['total_team_xp']}{RESET}  |  "
        f"{PURPLE}⚡ Team Level: {board['team_level']}{RESET}  |  "
        f"{CYAN}👑 MVP: {board['mvp_teammate']}{RESET}\n"
    )

    print(
        f"{BOLD}{'Rank':<5} {'Teammate':<18} {'Level / Title':<26} {'XP':<9} {'Cheers':<8} {'Autobot Companion':<24}{RESET}"
    )
    print(f"{DIM}{'─' * 90}{RESET}")

    medals = ["🥇", "🥈", "🥉", " 4.", " 5.", " 6."]
    for idx, s in enumerate(board["standings"]):
        m = medals[idx] if idx < len(medals) else f" {idx + 1}."
        lvl_str = f"Lv.{s['level']} {s['level_title']}"
        xp_str = f"{s['xp']} XP"
        cheers_str = f"{s['cheers_received']} 🙌"
        color = GREEN if idx == 0 else (CYAN if idx in (1, 2) else RESET)
        print(
            f"{color}{m:<5} {s['name']:<18} {lvl_str:<26} {xp_str:<9} {cheers_str:<8} {s['autobot_companion']}{RESET}"
        )

    print(f"\n{BOLD}🎯 Active Team Badges & Quests Summary:{RESET}")
    completed_q = sum(1 for q in board["quests"] if q["completed"])
    total_q = len(board["quests"])
    print(f"  • Quests Unlocked: {GREEN}{completed_q} / {total_q}{RESET}")
    print(f"  • Leaderboard Web Arcade: {BLUE}open frontend/leaderboard.html{RESET}")
    print(f"  • High-Five Teammate:     {YELLOW}npx hsf cheer <teammate-name>{RESET}\n")


def show_quests():
    engine = GamificationEngine()
    board = engine.get_leaderboard()

    print(f"\n{CYAN}🎯 HSF 24-HOUR HACKATHON QUESTS & BOUNTIES{RESET}\n")
    for q in board["quests"]:
        status = (
            f"{GREEN}✔ COMPLETED{RESET}" if q["completed"] else f"{YELLOW}⏳ ACTIVE BOUNTY{RESET}"
        )
        by = f" {DIM}(by {', '.join(q['completed_by'])}){RESET}" if q["completed_by"] else ""
        print(
            f"{BOLD}[{q['id']}]{RESET} {q['title']}  {PURPLE}+{q['xp_reward']} XP{RESET}  {q['badge']}  |  {status}{by}"
        )
        print(f"     {DIM}{q['description']}{RESET}\n")

    print(
        f'{CYAN}Claim bounty via:{RESET} {YELLOW}npx hsf quest claim <quest-id> --teammate "Your Name"{RESET}\n'
    )


def claim_quest(quest_id: str, teammate_name: str):
    engine = GamificationEngine()
    res = engine.claim_quest(quest_id, teammate_name)
    if res.get("success"):
        print(f"\n{GREEN}🎉 {res['message']}{RESET}")
        print(
            f"⭐ XP Awarded: {PURPLE}+{res['xp_awarded']}{RESET} | Total XP: {res['total_xp']} (Level {res['level']} {res['level_title']})"
        )
        print(f"🎖️ Badge Unlocked: {res['badge']}\n")
    else:
        print(f"\n{YELLOW}ℹ {res.get('message') or res.get('error')}{RESET}\n")


def cheer_teammate(sender: str, receiver: str):
    engine = GamificationEngine()
    res = engine.cheer_teammate(sender, receiver)
    if res.get("success"):
        print(f"\n{GREEN}🎉 {res['message']}{RESET}\n")
    else:
        print(f"\n{YELLOW}❌ {res.get('error')}{RESET}\n")


def main():
    parser = argparse.ArgumentParser(description="HSF Gamification & Teammate Leaderboard CLI")
    subparsers = parser.add_subparsers(dest="action")

    # leaderboard
    subparsers.add_parser("board")

    # quests
    subparsers.add_parser("quests")

    # claim
    claim_p = subparsers.add_parser("claim")
    claim_p.add_argument("quest_id", help="ID of quest (e.g. q-ignition)")
    claim_p.add_argument(
        "--teammate", default="Lead Architect", help="Teammate name claiming quest"
    )

    # cheer
    cheer_p = subparsers.add_parser("cheer")
    cheer_p.add_argument("receiver", help="Teammate to cheer")
    cheer_p.add_argument("--sender", default="Orbit Mascot", help="Sender name")

    args = parser.parse_args()

    if args.action == "quests":
        show_quests()
    elif args.action == "claim":
        claim_quest(args.quest_id, args.teammate)
    elif args.action == "cheer":
        cheer_teammate(args.sender, args.receiver)
    else:
        show_leaderboard()


if __name__ == "__main__":
    main()
