from typing import Protocol, Optional
from core.models.auth import User, LoginRequest


class IAuthRepository(Protocol):
    """Authentication repository interface - will be implemented by Cognito"""
    
    async def authenticate_user(self, login_request: LoginRequest) -> Optional[User]:
        """Authenticate user credentials and return user if valid"""
        ...
    
    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        ...
    
    async def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        ...
    
    async def create_user(self, username: str, email: str, password: str) -> User:
        """Create new user account"""
        ...
    
    async def update_user(self, user: User) -> User:
        """Update user information"""
        ...
    
    async def delete_user(self, user_id: str) -> bool:
        """Delete user account"""
        ...
    
    async def refresh_token(self, refresh_token: str) -> Optional[dict]:
        """Refresh access token using refresh token"""
        ...
