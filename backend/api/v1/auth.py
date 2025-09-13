from fastapi import APIRouter, Depends, HTTPException, status
from core.models.auth import LoginRequest, LoginResponse, TokenRefreshRequest, TokenResponse, User
from core.services.auth_service import AuthService
from shared.dependencies.auth import get_auth_service, get_current_user, get_current_admin_user


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=LoginResponse)
async def login(
    login_request: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Authenticate user and return JWT tokens"""
    result = await auth_service.login(login_request)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    return result


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_request: TokenRefreshRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Refresh access token using refresh token"""
    result = await auth_service.refresh_token(refresh_request.refresh_token)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    return result


@router.get("/me", response_model=User)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """Get current authenticated user information"""
    return current_user


@router.post("/logout")
async def logout():
    """Logout user (client should discard tokens)"""
    # In a full implementation, you might want to blacklist the token
    # For JWT, typically handled client-side by discarding tokens
    return {"message": "Successfully logged out"}


# Admin-only endpoint example
@router.get("/admin/users")
async def get_all_users(
    admin_user: User = Depends(get_current_admin_user)
):
    """Get all users (admin only)"""
    # This would call a user repository to get all users
    return {"message": "Admin endpoint - would return all users"}
