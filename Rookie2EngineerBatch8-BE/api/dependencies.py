from database.db import get_db
from core.config import settings
from schemas.user import UserRead
from fastapi import Depends
from core.exceptions import AuthenticationException, PermissionDeniedException, NotFoundException
from jose import jwt
from services.user import UserService
from enums.user.type import Type
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from fastapi import Request, HTTPException
from typing import Optional


class OAuth2PasswordBearerWithCookie(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> Optional[str]:
        # First try to get token from header (default OAuth2PasswordBearer behavior)
        try:
            token = await super().__call__(request)
            return token
        except HTTPException:
            # If no valid Authorization header found, try cookie
            token = request.cookies.get("access_token")
            if not token:
                if self.auto_error:
                    raise HTTPException(
                        status_code=401,
                        detail="Not authenticated",
                        headers={"WWW-Authenticate": "Bearer"},
                    )
                else:
                    return None
            return token


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/v1/auth/login")


def get_db_session():
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_session)) -> UserRead:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except jwt.JWTError:
        raise AuthenticationException()

    user = UserService(db).get_user_by_username(payload.get("sub"))
    if not user:
        raise NotFoundException(detail="User not found")
    return user


async def get_current_admin(current_user: UserRead = Depends(get_current_user)) -> UserRead:
    if current_user.type != Type.ADMIN:
        raise PermissionDeniedException(detail="Admin permission required")
    return current_user
