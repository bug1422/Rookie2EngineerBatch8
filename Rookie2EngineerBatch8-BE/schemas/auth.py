from pydantic import BaseModel
from enums.user.type import Type
from enums.shared.location import Location
class TokenPayload(BaseModel):
    sub: str  # Subject (username)
    exp: int  # Expiry timestamp
    user_id: int


class AccessTokenPayload(TokenPayload):
    first_name: str
    last_name: str
    type: Type
    is_first_login: bool
    location: Location


class RefreshTokenPayload(TokenPayload):
    jti: str  # Unique ID to revoke or identify the token


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    username: str
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str