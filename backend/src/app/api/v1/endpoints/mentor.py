import sys
from pathlib import Path
from typing import Any, Dict, List

from fastapi import APIRouter
from src.app.schemas.common import ResponseEnvelope

# Ensure repo root is on path for ai_layer imports
REPO_ROOT = Path(__file__).resolve().parents[5]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ai_layer.mentor_orchestrator import (  # noqa: E402
    MentoringConsultationRequest,
    MultiAgentMentorOrchestrator,
)

router = APIRouter()


@router.post("/orchestrate", response_model=ResponseEnvelope[Dict[str, Any]])
async def orchestrate_mentoring(request: MentoringConsultationRequest):
    """
    Dynamically triggers multi-agent mentoring across:
    1. Persona Copilot (Optimus, Ironhide, Bumblebee, Wheeljack, Mirage)
    2. Architecture Supervisor Sentinel
    3. Peer Synergy Coordinator
    4. Action Item Dispatcher
    """
    session = MultiAgentMentorOrchestrator.orchestrate(request)
    return ResponseEnvelope(
        data=session.model_dump(),
        message=f"Multi-agent mentoring orchestrated successfully for {request.teammate_name} ({request.role})",
    )


@router.get("/stages", response_model=ResponseEnvelope[List[Dict[str, Any]]])
async def list_mentoring_stages():
    """Returns the 6 end-to-end hackathon mentoring stages from Hour 0 to Hour 24."""
    stages = [s.model_dump() for s in MultiAgentMentorOrchestrator.get_stages()]
    return ResponseEnvelope(data=stages, message="Mentoring stages retrieved successfully")


@router.get("/roles", response_model=ResponseEnvelope[List[Dict[str, Any]]])
async def list_mentoring_roles():
    """Returns the available teammate roles and paired Autobot companions."""
    roles = [r.model_dump() for r in MultiAgentMentorOrchestrator.get_roles()]
    return ResponseEnvelope(data=roles, message="Mentoring roles retrieved successfully")
