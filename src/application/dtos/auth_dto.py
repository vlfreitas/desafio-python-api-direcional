from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    """Token schema."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token data schema."""

    username: str | None = None


class UserLogin(BaseModel):
    """User login schema."""

    username: str
    password: str


class UserCreate(BaseModel):
    """User creation schema."""

    username: str
    email: EmailStr
    password: str
