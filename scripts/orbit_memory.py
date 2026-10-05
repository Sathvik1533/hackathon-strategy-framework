"""
Orbit Memory CLI Tool
(scripts/orbit_memory.py)

Inspects Orbit's developer telemetry traces and cognitive memory state.
"""

import os
import sys

# Ensure repository root is on PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_layer.orbit_memory_tracer import OrbitMemoryTracer


def main():
    tracer = OrbitMemoryTracer()
    mem = tracer.get_memory_summary()
    traces = tracer.get_recent_traces(10)

    print("\n🧠 SENIOR ORBIT DEVELOPER TELEMETRY & MEMORY ENGINE")
    print("=" * 60)
    print(f"Total Interactions Logged: {mem['total_interactions']}")
    print(f"System Health Index:       {mem['system_health_index'] * 100:.1f}%")
    print(
        f"Tracked Teammates:         {len(mem['teammates_tracked'])} ({', '.join(mem['teammates_tracked'].keys()) or 'None'})"
    )
    print(f"Learned Team Bottlenecks:  {len(mem['common_team_bottlenecks'])}")
    for p in mem["common_team_bottlenecks"]:
        print(f"  • [{p['pattern_id']}] {p['observation']} (Occurrences: {p['occurrences_count']})")

    print("\n📜 Recent Telemetry Traces Stream (.hsf/traces.jsonl):")
    if not traces:
        print(
            "  (No traces recorded yet. Pair with Senior Orbit or run hsf squad to generate traces.)"
        )
    for t in traces:
        risks = f" [Flagged: {', '.join(t.detected_risks)}]" if t.detected_risks else ""
        print(
            f"  [{t.trace_id}] {t.teammate_name} ({t.active_branch}) -> {t.action_type}: {t.query_or_task[:60]}{risks}"
        )
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
