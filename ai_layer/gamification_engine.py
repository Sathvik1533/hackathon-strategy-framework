#!/usr/bin/env python3
"""
HSF Gamification & Teammate Arena Engine.
Transforms hackathon sprint execution into an interactive, collaborative gaming experience.
Tracks teammate XP, Levels, Autobot Synergy, Quests/Bounties, Badges, and Real-Time Leaderboards.
State is persisted in `.hsf/gamification.json`.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

HSF_DIR = Path(".hsf")
GAMIFICATION_FILE = HSF_DIR / "gamification.json"


class Quest(BaseModel):
    id: str
    title: str
    description: str
    category: str
    xp_reward: int
    badge: str
    completed_by: List[str] = Field(default_factory=list)
    completed: bool = False
    completed_at: Optional[str] = None


class TeammateStats(BaseModel):
    name: str
    role: str
    autobot_companion: str
    xp: int = 0
    level: int = 1
    level_title: str = "Cadet Novice"
    quests_completed: int = 0
    cheers_received: int = 0
    synergy_streak: int = 1
    badges: List[str] = Field(default_factory=list)
    recent_activity: List[str] = Field(default_factory=list)


class GamificationState(BaseModel):
    team_name: str = "Cybertronian Pentad"
    total_team_xp: int = 0
    team_level: int = 1
    mvp_teammate: Optional[str] = None
    teammates: Dict[str, TeammateStats] = Field(default_factory=dict)
    quests: List[Quest] = Field(default_factory=list)
    last_updated: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


DEFAULT_QUESTS = [
    Quest(
        id="q-ignition",
        title="Ignition Sequence",
        description="Run ./init.sh and verify local Docker stack & health checks in under 60 seconds.",
        category="DevOps",
        xp_reward=100,
        badge="🚀 Ignite Master"
    ),
    Quest(
        id="q-autobot",
        title="Autobot Alliance",
        description="Run hsf wizard, choose role, pair with an Autobot companion, and acquire .hsf prompt.",
        category="Coordination",
        xp_reward=150,
        badge="🤖 Autobot Bonded"
    ),
    Quest(
        id="q-contract",
        title="Zero-Collision Contract",
        description="Define an OpenAPI 3.1 Pydantic schema or Supabase RLS security policy with zero type errors.",
        category="Backend & DB",
        xp_reward=200,
        badge="🛡️ Contract Sentinel"
    ),
    Quest(
        id="q-neural-strike",
        title="Neural Strike RAG",
        description="Execute hybrid dense HNSW + sparse BM25 query with FlashRank cross-encoder latency < 20ms.",
        category="AI & Data",
        xp_reward=250,
        badge="⚡ Neural Marksman"
    ),
    Quest(
        id="q-resilience-fortress",
        title="Resilience Fortress",
        description="Trigger circuit breaker failover test and confirm automated 3-state recovery and local fallback.",
        category="Resilience",
        xp_reward=300,
        badge="🏰 Citadel Defender"
    ),
    Quest(
        id="q-eval-supremacy",
        title="Eval Supremacy",
        description="Run RAGAS evaluation harness and verify Faithfulness score >= 0.90 on 25 golden cases.",
        category="Evals & QA",
        xp_reward=350,
        badge="🎯 Truth Seeker"
    ),
    Quest(
        id="q-shadow-runner",
        title="Stage Shadow Runner",
        description="Execute offline stage runner (pitch/demo.sh) locally in <30 seconds with 0ms internet dependency.",
        category="Stage Defense",
        xp_reward=400,
        badge="🕶️ Shadow Ghost"
    ),
    Quest(
        id="q-stage-victory",
        title="Stage Victory Rehearsal",
        description="Complete 6-minute live pitch rehearsal simulator with 0 judge critical flags.",
        category="Stage Victory",
        xp_reward=500,
        badge="🏆 Champion of Orbit"
    )
]

DEFAULT_TEAMMATES = {
    "Lead Architect": TeammateStats(
        name="Lead Architect",
        role="Lead System Architect",
        autobot_companion="Orbit Prime 🤖👑",
        xp=450,
        level=2,
        level_title="Tactical Strategist",
        quests_completed=2,
        cheers_received=3,
        badges=["🤖 Autobot Bonded", "🚀 Ignite Master"],
        recent_activity=["Bootstrapped HSF stack in 48s", "Paired with Orbit Prime"]
    ),
    "Backend Lead": TeammateStats(
        name="Backend Lead",
        role="Backend & Security Lead",
        autobot_companion="Ironhide 🛡️⚡",
        xp=650,
        level=3,
        level_title="Resilience Titan",
        quests_completed=3,
        cheers_received=4,
        badges=["🛡️ Contract Sentinel", "🏰 Citadel Defender"],
        recent_activity=["Hardened circuit breaker failover", "Verified 19/19 pytest pass rate"]
    ),
    "Frontend Lead": TeammateStats(
        name="Frontend Lead",
        role="Frontend & UX Lead",
        autobot_companion="Mirage 🎨✨",
        xp=500,
        level=2,
        level_title="Hologram Artisan",
        quests_completed=2,
        cheers_received=5,
        badges=["🎨 Aesthetic Visionary", "🚀 Ignite Master"],
        recent_activity=["Deployed Next.js Motion HUD", "Crafted Glassmorphic design tokens"]
    ),
    "AI Lead": TeammateStats(
        name="AI Lead",
        role="AI & Multi-Agent Lead",
        autobot_companion="Wheeljack 🔬⚡",
        xp=850,
        level=4,
        level_title="Cyber-Scientist",
        quests_completed=4,
        cheers_received=6,
        badges=["⚡ Neural Marksman", "🎯 Truth Seeker"],
        recent_activity=["Verified RAGAS Faithfulness 0.94", "Benchmarked FlashRank CPU latency 16ms"]
    ),
    "DevOps Lead": TeammateStats(
        name="DevOps Lead",
        role="DevOps & Stage Lead",
        autobot_companion="Bumblebee 🐝🚀",
        xp=600,
        level=3,
        level_title="Stage Commander",
        quests_completed=3,
        cheers_received=4,
        badges=["🕶️ Shadow Ghost", "🚀 Ignite Master"],
        recent_activity=["Compiled Marp pitch deck in 1.8s", "Tested offline pitch/demo.sh runner"]
    )
}


class GamificationEngine:
    def __init__(self, state_file: Path = GAMIFICATION_FILE):
        self.state_file = state_file
        self.state = self._load_or_initialize()

    def _calculate_level(self, xp: int) -> tuple[int, str]:
        if xp >= 1500:
            return 5, "Cybertronian Grandmaster"
        elif xp >= 1000:
            return 4, "Cyber-Scientist Elite"
        elif xp >= 600:
            return 3, "Resilience Titan"
        elif xp >= 300:
            return 2, "Tactical Strategist"
        else:
            return 1, "Cadet Novice"

    def _load_or_initialize(self) -> GamificationState:
        if self.state_file.exists():
            try:
                data = json.loads(self.state_file.read_text(encoding="utf-8"))
                return GamificationState(**data)
            except Exception:
                pass

        # Initialize default state
        state = GamificationState(
            team_name="Autobots Strike Fleet",
            total_team_xp=sum(t.xp for t in DEFAULT_TEAMMATES.values()),
            team_level=3,
            mvp_teammate="AI Lead",
            teammates=DEFAULT_TEAMMATES,
            quests=DEFAULT_QUESTS
        )
        self._save(state)
        return state

    def _save(self, state: Optional[GamificationState] = None):
        if state is None:
            state = self.state
        state.last_updated = datetime.now(timezone.utc).isoformat()
        HSF_DIR.mkdir(parents=True, exist_ok=True)
        self.state_file.write_text(json.dumps(state.model_dump(), indent=2), encoding="utf-8")

    def get_leaderboard(self) -> Dict[str, Any]:
        """Returns sorted teammate standings and team metrics."""
        ranked = sorted(
            self.state.teammates.values(),
            key=lambda t: (t.xp, t.cheers_received, t.quests_completed),
            reverse=True
        )

        # Update MVP and team totals
        if ranked:
            self.state.mvp_teammate = ranked[0].name
        self.state.total_team_xp = sum(t.xp for t in self.state.teammates.values())
        self.state.team_level = max(1, self.state.total_team_xp // 1000 + 1)
        self._save()

        return {
            "team_name": self.state.team_name,
            "total_team_xp": self.state.total_team_xp,
            "team_level": self.state.team_level,
            "mvp_teammate": self.state.mvp_teammate,
            "standings": [t.model_dump() for t in ranked],
            "quests": [q.model_dump() for q in self.state.quests],
            "last_updated": self.state.last_updated
        }

    def claim_quest(self, quest_id: str, teammate_name: str) -> Dict[str, Any]:
        """Award quest XP, badges and level up a teammate."""
        quest = next((q for q in self.state.quests if q.id == quest_id), None)
        if not quest:
            return {"success": False, "error": f"Quest '{quest_id}' not found."}

        # Normalize teammate name or create if new
        matched_key = None
        for k in self.state.teammates:
            if k.lower() == teammate_name.lower():
                matched_key = k
                break

        if not matched_key:
            matched_key = teammate_name
            self.state.teammates[matched_key] = TeammateStats(
                name=teammate_name,
                role="Operative",
                autobot_companion="Orbit Prime 🤖👑"
            )

        teammate = self.state.teammates[matched_key]

        # Check if already claimed by this teammate
        if teammate_name in quest.completed_by:
            return {
                "success": False,
                "message": f"Quest '{quest.title}' was already completed by {teammate.name}."
            }

        quest.completed_by.append(teammate.name)
        quest.completed = True
        quest.completed_at = datetime.now(timezone.utc).isoformat()

        # Award XP and badge
        teammate.xp += quest.xp_reward
        teammate.quests_completed += 1
        if quest.badge not in teammate.badges:
            teammate.badges.append(quest.badge)

        # Recalculate level
        new_lvl, new_title = self._calculate_level(teammate.xp)
        leveled_up = new_lvl > teammate.level
        teammate.level = new_lvl
        teammate.level_title = new_title

        activity_msg = f"Completed Quest: {quest.title} (+{quest.xp_reward} XP)"
        teammate.recent_activity.insert(0, activity_msg)
        if len(teammate.recent_activity) > 5:
            teammate.recent_activity = teammate.recent_activity[:5]

        self._save()

        return {
            "success": True,
            "message": f"🎉 Quest '{quest.title}' claimed by {teammate.name}!",
            "xp_awarded": quest.xp_reward,
            "total_xp": teammate.xp,
            "level": teammate.level,
            "level_title": teammate.level_title,
            "leveled_up": leveled_up,
            "badge": quest.badge
        }

    def cheer_teammate(self, sender: str, receiver_name: str) -> Dict[str, Any]:
        """Send a high-five or synergy cheer to a teammate (+25 XP each)."""
        matched_key = None
        for k in self.state.teammates:
            if k.lower() == receiver_name.lower():
                matched_key = k
                break

        if not matched_key:
            return {"success": False, "error": f"Teammate '{receiver_name}' not found."}

        receiver = self.state.teammates[matched_key]
        receiver.cheers_received += 1
        receiver.xp += 25
        receiver.synergy_streak += 1
        receiver.recent_activity.insert(0, f"Cheered by {sender} (+25 Synergy XP)")

        # Recalculate level
        receiver.level, receiver.level_title = self._calculate_level(receiver.xp)

        self._save()
        return {
            "success": True,
            "message": f"🙌 {sender} cheered {receiver.name}! Synergy boosted (+25 XP).",
            "cheers_received": receiver.cheers_received,
            "receiver_xp": receiver.xp
        }


if __name__ == "__main__":
    engine = GamificationEngine()
    board = engine.get_leaderboard()
    print(f"Team: {board['team_name']} | Total XP: {board['total_team_xp']} | MVP: {board['mvp_teammate']}")
    for idx, s in enumerate(board["standings"], 1):
        print(f"#{idx} {s['name']} (Lv {s['level']} {s['level_title']}) - {s['xp']} XP | {s['autobot_companion']}")
