import sys
from pathlib import Path
from typing import Any, Dict

from fastapi import APIRouter
from pydantic import BaseModel, Field
from src.app.schemas.common import ResponseEnvelope

# Ensure repo root is on path for ai_layer imports
REPO_ROOT = Path(__file__).resolve().parents[5]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ai_layer.gamification_engine import GamificationEngine  # noqa: E402

router = APIRouter()
engine = GamificationEngine()


class ClaimQuestRequest(BaseModel):
    quest_id: str = Field(..., description="ID of the quest to claim (e.g., q-ignition)")
    teammate_name: str = Field(..., description="Name of the teammate claiming the quest")


class CheerRequest(BaseModel):
    sender: str = Field(default="Orbit Mascot", description="Name of the teammate sending cheer")
    receiver_name: str = Field(..., description="Name of the teammate receiving cheer")


@router.get("/leaderboard", response_model=ResponseEnvelope[Dict[str, Any]])
async def get_leaderboard():
    """Returns real-time teammate rankings, XP, Levels, and active quests."""
    data = engine.get_leaderboard()
    return ResponseEnvelope(data=data, message="Leaderboard retrieved successfully")


@router.get("/quests", response_model=ResponseEnvelope[list[Dict[str, Any]]])
async def list_quests():
    """Returns the catalog of 8 hackathon quests and completion status."""
    board = engine.get_leaderboard()
    return ResponseEnvelope(data=board["quests"], message="Quests retrieved successfully")


@router.post("/claim-quest", response_model=ResponseEnvelope[Dict[str, Any]])
async def claim_quest(payload: ClaimQuestRequest):
    """Awards XP, badges and levels up a teammate upon quest completion."""
    res = engine.claim_quest(payload.quest_id, payload.teammate_name)
    if not res.get("success"):
        return ResponseEnvelope(
            success=False, data=res, message=res.get("message") or res.get("error")
        )
    return ResponseEnvelope(data=res, message=res.get("message"))


@router.post("/cheer", response_model=ResponseEnvelope[Dict[str, Any]])
async def cheer_teammate(payload: CheerRequest):
    """Sends a high-five or synergy cheer to a teammate, granting +25 XP."""
    res = engine.cheer_teammate(payload.sender, payload.receiver_name)
    if not res.get("success"):
        return ResponseEnvelope(success=False, data=res, message=res.get("error"))
    return ResponseEnvelope(data=res, message=res.get("message"))
