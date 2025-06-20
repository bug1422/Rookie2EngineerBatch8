from fastapi import APIRouter, Depends, Response, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from services.auth import AuthService
from schemas.auth import TokenResponse, ChangePasswordRequest
from api.dependencies import get_db_session
from schemas.user import UserRead
from api.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=TokenResponse)
def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db_session),
   
    
):
    """
    Login endpoint to authenticate users and issue tokens

    Args:
        response: FastAPI response object for setting cookies
        form_data: Form with username and password
        db: Database session

    Returns:
        TokenResponse with access and refresh tokens
    """
    # Optional: Add a check using current_user if needed
    return AuthService(db).login(form_data.username, form_data.password, response)

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    response: Response,
    request: Request,
    db: Session = Depends(get_db_session)
):
    """
    Refresh token endpoint to issue new tokens

    Args:
        response: FastAPI response object for setting cookies
        request: FastAPI request object for getting cookies/body
        db: Database session

    Returns:
        TokenResponse with new access and refresh tokens
    """
    return await AuthService(db).refresh_token(response, request)

@router.post("/logout")
async def logout(
    response: Response,
    request: Request,
    db: Session = Depends(get_db_session)
):
    """
    Logout endpoint to clear cookies and revoke refresh token

    Args:
        response: FastAPI response object for clearing cookies
        request: FastAPI request object for getting cookies/body
        db: Database session

    Returns:
        Success message
    """
    return await AuthService(db).logout(response, request)

@router.post("/change-password", status_code=status.HTTP_200_OK)
def change_password(
    payload: ChangePasswordRequest,
    db: Session = Depends(get_db_session),
    current_user = Depends(get_current_user)
):
    """
    Đổi mật khẩu cho user đã đăng nhập.
    """
    return AuthService(db).change_password(
        user=current_user,
        old_password=payload.old_password,
        new_password=payload.new_password
    )
    
@router.get("/check", status_code=status.HTTP_200_OK)
async def check_auth(user: UserRead = Depends(get_current_user)):
    return {"message": "You are authenticated"}