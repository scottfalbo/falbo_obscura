from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from core.models.auth import User
from core.services.auth_service import AuthService
from shared.utils.jwt_manager import jwt_manager


# FastAPI security scheme
security = HTTPBearer()


async def get_auth_service() -> AuthService:
    """Dependency to get auth service - will be configured with Cognito later"""
    # For now, return None - we'll wire this up when we implement Cognito
    # This is where we'll inject the Cognito repository implementation
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Auth service not yet configured with AWS Cognito"
    )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service)
) -> User:
    """Dependency to get current authenticated user from JWT token"""
    token = credentials.credentials
    
    user = await auth_service.get_current_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


async def get_current_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Dependency to get current user and verify admin privileges"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    
    return current_user


async def get_optional_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[User]:
    """Dependency to optionally get current user (doesn't fail if no token)"""
    if not credentials:
        return None
    
    token_payload = jwt_manager.verify_token(credentials.credentials)
    if not token_payload:
        return None
    
    # In a real implementation, we'd get user from repository
    # For now, create a mock user from token payload
    return User(
        id=token_payload.sub,
        username=token_payload.username,
        email=token_payload.email,
        is_admin=token_payload.is_admin,
        is_active=True,
        created_at=token_payload.iat,
        updated_at=token_payload.iat
    )
