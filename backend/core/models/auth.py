from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class User(BaseModel):
    """User domain model"""
    id: str
    username: str
    email: EmailStr
    is_active: bool = True
    is_admin: bool = False
    created_at: datetime
    updated_at: datetime


class LoginRequest(BaseModel):
    """Login request DTO"""
    username: str
    password: str


class LoginResponse(BaseModel):
    """Login response DTO"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds
    user: User


class TokenRefreshRequest(BaseModel):
    """Token refresh request DTO"""
    refresh_token: str


class TokenResponse(BaseModel):
    """Token response DTO"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenPayload(BaseModel):
    """JWT token payload"""
    sub: str  # user id
    username: str
    email: str
    is_admin: bool = False
    exp: datetime
    iat: datetime
