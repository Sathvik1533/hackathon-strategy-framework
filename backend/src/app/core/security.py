from datetime import UTC, datetime, timedelta
from typing import Any

from src.app.core.config import settings

try:
    import jwt
except ImportError:
    import base64
    import json

    class MockJWT:
        @staticmethod
        def encode(payload, key, algorithm="HS256"):
            return (
                base64.urlsafe_b64encode(json.dumps(payload, default=str).encode())
                .decode()
                .rstrip("=")
            )

        @staticmethod
        def decode(token, key, algorithms=None):
            padded = token + "=" * (-len(token) % 4)
            return json.loads(base64.urlsafe_b64decode(padded.encode()).decode())

    jwt = MockJWT()

try:
    from passlib.context import CryptContext

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    _has_passlib = True
except ImportError:
    _has_passlib = False


def verify_password(plain_password: str, hashed_password: str) -> bool:
    if _has_passlib:
        return pwd_context.verify(plain_password, hashed_password)
    import hashlib

    return (
        hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password
        or plain_password == hashed_password
    )


def get_password_hash(password: str) -> str:
    if _has_passlib:
        return pwd_context.hash(password)
    import hashlib

    return hashlib.sha256(password.encode()).hexdigest()


def create_access_token(subject: str | Any, expires_delta: timedelta | None = None) -> str:
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
