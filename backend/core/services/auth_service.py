from typing import Optional
from core.interfaces.auth_repository import IAuthRepository
from core.models.auth import User, LoginRequest, LoginResponse, TokenResponse
from shared.utils.jwt_manager import jwt_manager


class AuthService:
    """Authentication business logic service"""
    
    def __init__(self, auth_repository: IAuthRepository):
        self.auth_repository = auth_repository
    
    async def login(self, login_request: LoginRequest) -> Optional[LoginResponse]:
        """Authenticate user and return tokens"""
        # Authenticate user through repository (will call Cognito)
        user = await self.auth_repository.authenticate_user(login_request)
        if not user:
            return None
        
        # Generate JWT tokens
        access_token = jwt_manager.create_access_token(user)
        refresh_token = jwt_manager.create_refresh_token(user)
        
        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=jwt_manager.access_token_expire_minutes * 60,
            user=user
        )
    
    async def refresh_token(self, refresh_token: str) -> Optional[TokenResponse]:
        """Refresh access token using refresh token"""
        # Verify refresh token
        token_payload = jwt_manager.verify_token(refresh_token)
        if not token_payload:
            return None
        
        # Get user to create new access token
        user = await self.auth_repository.get_user_by_id(token_payload.sub)
        if not user:
            return None
        
        # Generate new access token
        new_access_token = jwt_manager.create_access_token(user)
        
        return TokenResponse(
            access_token=new_access_token,
            expires_in=jwt_manager.access_token_expire_minutes * 60
        )
    
    async def get_current_user(self, token: str) -> Optional[User]:
        """Get current user from JWT token"""
        # Verify token
        token_payload = jwt_manager.verify_token(token)
        if not token_payload:
            return None
        
        # Get user from repository
        return await self.auth_repository.get_user_by_id(token_payload.sub)
    
    async def create_user(self, username: str, email: str, password: str) -> Optional[User]:
        """Create new user account"""
        return await self.auth_repository.create_user(username, email, password)
