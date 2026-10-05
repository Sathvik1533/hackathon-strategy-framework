"""
Orbit Persistent Memory & Developer Telemetry Tracer
(ai_layer/orbit_memory_tracer.py)

Maintains persistent developer interaction logs, code inspection traces,
and learned team behavioral patterns in .hsf/traces.jsonl and .hsf/memory.json.
Enables Senior Orbit to continuously learn from past developer mistakes,
track velocity milestones, and recall contextual advice dynamically.
"""

from __future__ import annotations

import json
import os
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class TelemetryTrace(BaseModel):
    trace_id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    teammate_name: str
    role: str
    active_branch: str
    action_type: (
        str  # ONBOARDING, CODE_REVIEW, ARCHITECTURE_DECISION, GUARDRAIL_ALERT, REPAIR_ADVICE
    )
    query_or_task: str
    code_inspected: Optional[str] = None
    guidance_rendered: str
    detected_risks: List[str] = Field(default_factory=list)
    outcome_status: str = "RESOLVED"  # RESOLVED, IN_PROGRESS, FLAGGED


class LearnedTeamPattern(BaseModel):
    pattern_id: str
    category: str
    observation: str
    recommended_mitigation: str
    occurrences_count: int = 1
    last_observed_timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


class OrbitMemoryState(BaseModel):
    total_interactions: int = 0
    teammates_tracked: Dict[str, Dict] = Field(default_factory=dict)
    common_team_bottlenecks: List[LearnedTeamPattern] = Field(default_factory=list)
    system_health_index: float = 1.0  # 0.0 to 1.0 based on compliance rate


class OrbitMemoryTracer:
    """
    Persistent tracer and cognitive learning engine for Orbit.
    Saves traces to .hsf/traces.jsonl and memory state to .hsf/memory.json.
    """

    def __init__(self, data_dir: str = ".hsf"):
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)
        self.traces_file = os.path.join(self.data_dir, "traces.jsonl")
        self.memory_file = os.path.join(self.data_dir, "memory.json")
        self.state = self._load_state()

    def _load_state(self) -> OrbitMemoryState:
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return OrbitMemoryState(**data)
            except Exception:
                pass
        return OrbitMemoryState()

    def _save_state(self):
        try:
            with open(self.memory_file, "w", encoding="utf-8") as f:
                json.dump(self.state.model_dump(), f, indent=2)
        except Exception as e:
            print(f"[OrbitMemoryTracer] Warning: Failed to save memory state: {e}")

    def log_trace(
        self,
        teammate_name: str,
        role: str,
        active_branch: str,
        action_type: str,
        query_or_task: str,
        guidance_rendered: str,
        code_inspected: Optional[str] = None,
        detected_risks: Optional[List[str]] = None,
        outcome_status: str = "RESOLVED",
    ) -> TelemetryTrace:
        """
        Records a single interaction trace and updates Orbit's learned memory models.
        """
        risks = detected_risks or []
        trace = TelemetryTrace(
            teammate_name=teammate_name,
            role=role,
            active_branch=active_branch,
            action_type=action_type,
            query_or_task=query_or_task,
            code_inspected=code_inspected,
            guidance_rendered=guidance_rendered,
            detected_risks=risks,
            outcome_status=outcome_status,
        )

        # 1. Append to traces.jsonl
        try:
            with open(self.traces_file, "a", encoding="utf-8") as f:
                f.write(trace.model_dump_json() + "\n")
        except Exception as e:
            print(f"[OrbitMemoryTracer] Warning: Failed to append trace: {e}")

        # 2. Update memory state
        self.state.total_interactions += 1
        t_key = teammate_name.lower().strip()
        if t_key not in self.state.teammates_tracked:
            self.state.teammates_tracked[t_key] = {
                "name": teammate_name,
                "role": role,
                "branches_worked": [active_branch],
                "total_queries": 1,
                "risks_flagged": len(risks),
                "first_seen": trace.timestamp,
                "last_active": trace.timestamp,
            }
        else:
            t_data = self.state.teammates_tracked[t_key]
            t_data["total_queries"] += 1
            t_data["risks_flagged"] += len(risks)
            t_data["last_active"] = trace.timestamp
            if active_branch not in t_data["branches_worked"]:
                t_data["branches_worked"].append(active_branch)

        # 3. Analyze recurring team patterns
        for r in risks:
            self._record_risk_pattern(r)

        self._save_state()
        return trace

    def _record_risk_pattern(self, risk_description: str):
        for pattern in self.state.common_team_bottlenecks:
            if (
                pattern.observation.lower() in risk_description.lower()
                or risk_description.lower() in pattern.observation.lower()
            ):
                pattern.occurrences_count += 1
                pattern.last_observed_timestamp = datetime.now(timezone.utc).isoformat()
                return

        new_pattern = LearnedTeamPattern(
            pattern_id=f"PAT-{len(self.state.common_team_bottlenecks) + 1:03d}",
            category="Code Quality & Resilience Guardrail",
            observation=risk_description,
            recommended_mitigation="Enforce automated pre-commit hook with ruff and parameterized query bindings.",
            occurrences_count=1,
        )
        self.state.common_team_bottlenecks.append(new_pattern)

    def get_recent_traces(self, limit: int = 20) -> List[TelemetryTrace]:
        traces = []
        if not os.path.exists(self.traces_file):
            return traces

        try:
            with open(self.traces_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
                for line in reversed(lines[-limit:]):
                    if line.strip():
                        traces.append(TelemetryTrace(**json.loads(line)))
        except Exception as e:
            print(f"[OrbitMemoryTracer] Warning: Failed to read traces: {e}")
        return traces

    def recall_context_for_teammate(
        self, teammate_name: str, active_branch: str, current_query: str
    ) -> List[str]:
        """
        Recalls relevant past guidance or recurring hurdles to enrich the senior response.
        """
        recalled: List[str] = []
        t_key = teammate_name.lower().strip()

        if t_key in self.state.teammates_tracked:
            info = self.state.teammates_tracked[t_key]
            recalled.append(
                f"🧠 Context Recall: Teammate {teammate_name} has {info['total_queries']} recorded pairing sessions across branches: {', '.join(info['branches_worked'])}."
            )

        # Scan recent traces for this teammate
        past_traces = self.get_recent_traces(limit=15)
        teammate_past = [t for t in past_traces if t.teammate_name.lower() == t_key]

        for pt in teammate_past[:3]:
            if pt.detected_risks:
                recalled.append(
                    f"⚠️ Reminder from previous trace '{pt.trace_id}': We flagged '{', '.join(pt.detected_risks)}'. Maintain guardrails!"
                )

        if self.state.common_team_bottlenecks:
            top_risk = max(self.state.common_team_bottlenecks, key=lambda p: p.occurrences_count)
            recalled.append(
                f"📈 Learned Squad Insight: '{top_risk.observation}' has been flagged {top_risk.occurrences_count}x across the team. Double check this layer."
            )

        return recalled

    def get_memory_summary(self) -> Dict[str, Any]:
        """
        Returns an aggregate summary of Orbit's cognitive memory state.
        """
        return {
            "total_interactions": self.state.total_interactions,
            "teammates_tracked": self.state.teammates_tracked,
            "common_team_bottlenecks": [p.model_dump() for p in self.state.common_team_bottlenecks],
            "system_health_index": self.state.system_health_index,
        }
