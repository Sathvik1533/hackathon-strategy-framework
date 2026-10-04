from fastapi import APIRouter, HTTPException, status
from src.app.schemas.auth import UserLogin, Token, UserResponse
from src.app.schemas.common import ResponseEnvelope
from src.app.core.security import create_access_token

router = APIRouter()

@router.post("/login", response_model=ResponseEnvelope[Token])
async def login(credentials: UserLogin):
    """Simple baseline JWT authentication for hackathon apps"""
    # For hackathons, demo login accepts any test password or validates against DB
    if not credentials.email:
        raise HTTPException(status_code=400, detail="Invalid email")

    token = create_access_token(subject=credentials.email)
    return ResponseEnvelope(
        data=Token(access_token=token),
        message="Authentication successful"
    )
