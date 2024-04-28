from uuid import UUID
from pydantic import BaseModel


class CustomOAuth2PasswordRequestForm(BaseModel):
    mobile: str
    password: str
    json_body: dict


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class RefreshTokenSchema(BaseModel):
    refresh_token: str


class TokenPayload(BaseModel):
    sub: UUID = None
    exp: int = None
    iat: int = None