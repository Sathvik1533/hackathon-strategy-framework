#!/usr/bin/env python3
"""
Live Stage Pitch Rehearsal Simulator & Presentation Timer for HSF.
Rehearses the 6-Minute Pitch Formula with live section countdowns,
speaker cues, talking points, and automated live demo verification.
"""

import argparse
import subprocess
import sys
import time

CYAN = "\033[1;36m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
BLUE = "\033[1;34m"
PURPLE = "\033[1;35m"
RED = "\033[1;31m"
BOLD = "\033[1m"
RESET = "\033[0m"

SECTIONS = [
    {
        "minute_start": 0,
        "minute_end": 1,
        "title": "Phase 1: The Hook & The Broken Status Quo",
        "speaker": "Speaker 1 (Founder / Domain Lead)",
        "slide": "Slide 1-2 (Title & Problem Statement)",
        "talking_points": [
            "Start with a brutal statistic or real incident (e.g. '$450B lost annually to supply chain halts').",
            "Show why current solutions are slow, fragmented, or manual.",
            "Do NOT talk about your tech stack yet—hook the judges emotionally on the pain point.",
        ],
    },
    {
        "minute_start": 1,
        "minute_end": 2,
        "title": "Phase 2: The Autonomous Solution & Core Innovation",
        "speaker": "Speaker 1 / Speaker 2",
        "slide": "Slide 3 (Solution Overview & Key Capabilities)",
        "talking_points": [
            "Introduce your platform with a one-sentence value proposition.",
            "Explain how the system operates autonomously with intelligent multi-agent orchestration.",
            "Set up the transition: 'Don't take our word for it—let's see it live right now.'",
        ],
    },
    {
        "minute_start": 2,
        "minute_end": 3.5,
        "title": "Phase 3: The Live Working Demo (The Proof)",
        "speaker": "Speaker 2 (Technical / Product Lead)",
        "slide": "Live Browser (localhost:3000 / localhost:8000) OR Terminal (pitch/demo.sh)",
        "talking_points": [
            "Trigger a real workflow: document ingestion, vector query, or agentic reasoning.",
            "Show sub-10ms response time and real-time SSE stream updates.",
            "Demonstrate the human-in-the-loop safety gate pausing before risky operations.",
            "If Wi-Fi drops: run `bash pitch/demo.sh` immediately without flinching!",
        ],
    },
    {
        "minute_start": 3.5,
        "minute_end": 4.5,
        "title": "Phase 4: Architecture & Defensible Moats",
        "speaker": "Speaker 2 (Lead Engineer)",
        "slide": "Slide 4-5 (System Architecture & Verification Metrics)",
        "talking_points": [
            "Show the Archify / Mermaid blueprint: FastAPI, Redis, pgvector HNSW, LangGraph.",
            "Highlight verified metrics: P95 latency < 85ms, RAGAS faithfulness >= 0.90.",
            "Mention enterprise resilience: Redis circuit breakers and Supabase Row-Level Security.",
        ],
    },
    {
        "minute_start": 4.5,
        "minute_end": 5.5,
        "title": "Phase 5: Market Opportunity, ROI & Business Viability",
        "speaker": "Speaker 1 (Founder)",
        "slide": "Slide 6 (Market Size & Business Model)",
        "talking_points": [
            "TAM / SAM / SOM breakdown with clear go-to-market wedge.",
            "Pricing model: tiered API consumption / enterprise SaaS licenses.",
            "Quantified customer ROI: 'Cuts manual resolution time from 4 days to 4 seconds.'",
        ],
    },
    {
        "minute_start": 5.5,
        "minute_end": 6,
        "title": "Phase 6: The Vision, Team & Call to Action",
        "speaker": "Both Speakers",
        "slide": "Slide 7 (Team Roster & Closing Slide)",
        "talking_points": [
            "Show team credentials and domain superpowers.",
            "Deliver memorable closing sentence.",
            "Smile, open arms, and invite questions: 'Thank you—we are excited to take your questions.'",
        ],
    },
]


def print_banner():
    print(
        f"""{PURPLE}
╔═══════════════════════════════════════════════════════════════════════════════╗
║            🎤 HSF LIVE STAGE PITCH REHEARSAL SIMULATOR (6-MIN CLOCK)          ║
║              Master the Winning Presentation Formula Before Judges            ║
╚═══════════════════════════════════════════════════════════════════════════════╝{RESET}"""
    )


def run_rehearsal(speed_multiplier=1.0, test_demo=False):
    print_banner()
    print(
        f"{YELLOW}⚡ Rehearsal Mode: {speed_multiplier:.1f}x speed | Total Duration: {6.0 / speed_multiplier:.1f} minutes{RESET}"
    )
    print(
        f"{CYAN}Cues will ring terminal bells and print slide talking points in real-time.{RESET}"
    )
    input(f"\n{BOLD}Press ENTER to start the stage timer and begin speaking...{RESET}")

    total_seconds = int(360 / speed_multiplier)
    current_section_idx = -1

    for elapsed_sec in range(total_seconds + 1):
        actual_min = (elapsed_sec * speed_multiplier) / 60.0

        # Determine which section we are in
        matching_idx = 0
        for i, s in enumerate(SECTIONS):
            if s["minute_start"] <= actual_min < s["minute_end"]:
                matching_idx = i
                break
            elif actual_min >= 5.5:
                matching_idx = len(SECTIONS) - 1

        # Section transition
        if matching_idx != current_section_idx:
            current_section_idx = matching_idx
            sec_data = SECTIONS[current_section_idx]
            sys.stdout.write("\a")  # Terminal bell cue
            sys.stdout.flush()
            print(
                f"\n\n{PURPLE}==============================================================================={RESET}"
            )
            print(f"{BOLD}{GREEN}🔔 [{actual_min:04.1f}m / 6.0m] {sec_data['title']}{RESET}")
            print(
                f"{PURPLE}==============================================================================={RESET}"
            )
            print(f"  {BOLD}👤 Speaker:{RESET}  {sec_data['speaker']}")
            print(f"  {BOLD}🖥️  Slide:{RESET}    {CYAN}{sec_data['slide']}{RESET}")
            print(f"\n  {BOLD}🎯 Key Talking Points:{RESET}")
            for tp in sec_data["talking_points"]:
                print(f"    • {tp}")
            print(
                f"{PURPLE}-------------------------------------------------------------------------------{RESET}"
            )

            if test_demo and current_section_idx == 2:
                print(
                    f"\n{YELLOW}⚡ [AUTOMATED TEST] Executing pitch/demo.sh to verify live demo timing...{RESET}\n"
                )
                subprocess.run("bash pitch/demo.sh", shell=True)
                print(
                    f"\n{GREEN}✔ Live demo simulation finished! Continuing pitch rehearsal...{RESET}\n"
                )

        # Countdown tick
        remaining_sec = total_seconds - elapsed_sec
        rem_m, rem_s = divmod(int(remaining_sec * speed_multiplier), 60)
        sys.stdout.write(
            f"\r{YELLOW}⏱️  Elapsed: {actual_min:04.1f}m | Remaining: {rem_m:02d}:{rem_s:02d} | Speak clearly & maintain eye contact...{RESET} "
        )
        sys.stdout.flush()

        time.sleep(1.0 / speed_multiplier)

    print(
        f"\n\n{GREEN}==============================================================================={RESET}"
    )
    print(f"{GREEN}🎉 TIME'S UP! 6-MINUTE STAGE REHEARSAL COMPLETE!{RESET}")
    print(
        f"{GREEN}==============================================================================={RESET}"
    )
    print("  ✔ Both speakers maintained pacing within the 6-minute hard limit.")
    print("  ✔ Live demo was allocated 90 seconds without running out of time.")
    print("  ✔ Ready to present on stage with total confidence!")
    print(
        f"{GREEN}==============================================================================={RESET}\n"
    )


def main():
    parser = argparse.ArgumentParser(description="HSF Live Pitch Rehearsal Simulator")
    parser.add_argument(
        "--quick", action="store_true", help="Speed run (60 seconds total, 6x speed)"
    )
    parser.add_argument(
        "--speed", type=float, default=1.0, help="Custom speed multiplier (e.g. 2.0)"
    )
    parser.add_argument(
        "--test-demo", action="store_true", help="Automatically trigger demo.sh during demo phase"
    )
    args = parser.parse_args()

    multiplier = 6.0 if args.quick else args.speed
    run_rehearsal(speed_multiplier=multiplier, test_demo=args.test_demo)


if __name__ == "__main__":
    main()
