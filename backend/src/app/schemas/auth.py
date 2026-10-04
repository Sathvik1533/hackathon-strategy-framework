from pydantic import BaseModel

try:
    import email_validator  # noqa: F401
    from pydantic import EmailStr
except ImportError:
    from pydantic import Field
    from typing_extensions import Annotated

    EmailStr = Annotated[str, Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")]


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str | None = None
