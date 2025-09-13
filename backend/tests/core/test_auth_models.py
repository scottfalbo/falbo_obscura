import pytest
from datetime import datetime
from pydantic import ValidationError
from core.models.auth import User, LoginRequest, LoginResponse, TokenRefreshRequest, TokenResponse, TokenPayload


@pytest.mark.unit
class TestAuthModels:
    
    def test_user_model_valid(self):
        """Test User model with valid data"""
        user_data = {
            "id": "user123",
            "username": "testuser",
            "email": "test@example.com",
            "is_active": True,
            "is_admin": False,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        user = User(**user_data)
        
        assert user.id == user_data["id"]
        assert user.username == user_data["username"]
        assert user.email == user_data["email"]
        assert user.is_active == user_data["is_active"]
        assert user.is_admin == user_data["is_admin"]
    
    def test_user_model_defaults(self):
        """Test User model default values"""
        user_data = {
            "id": "user123",
            "username": "testuser",
            "email": "test@example.com",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        user = User(**user_data)
        
        # Test defaults
        assert user.is_active == True
        assert user.is_admin == False
    
    def test_user_model_invalid_email(self):
        """Test User model with invalid email"""
        user_data = {
            "id": "user123",
            "username": "testuser",
            "email": "invalid-email",  # Invalid email format
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        with pytest.raises(ValidationError) as exc_info:
            User(**user_data)
        
        assert "email" in str(exc_info.value)
    
    def test_login_request_valid(self):
        """Test LoginRequest model with valid data"""
        login_data = {
            "username": "testuser",
            "password": "password123"
        }
        
        login_request = LoginRequest(**login_data)
        
        assert login_request.username == login_data["username"]
        assert login_request.password == login_data["password"]
    
    def test_login_request_missing_fields(self):
        """Test LoginRequest model with missing required fields"""
        # Missing password
        with pytest.raises(ValidationError) as exc_info:
            LoginRequest(username="testuser")
        
        assert "password" in str(exc_info.value)
        
        # Missing username
        with pytest.raises(ValidationError) as exc_info:
            LoginRequest(password="password123")
        
        assert "username" in str(exc_info.value)
    
    def test_login_response_valid(self):
        """Test LoginResponse model with valid data"""
        user_data = {
            "id": "user123",
            "username": "testuser",
            "email": "test@example.com",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        user = User(**user_data)
        
        response_data = {
            "access_token": "access.token.here",
            "refresh_token": "refresh.token.here",
            "expires_in": 900,
            "user": user
        }
        
        login_response = LoginResponse(**response_data)
        
        assert login_response.access_token == response_data["access_token"]
        assert login_response.refresh_token == response_data["refresh_token"]
        assert login_response.token_type == "bearer"  # Default value
        assert login_response.expires_in == response_data["expires_in"]
        assert login_response.user.id == user.id
    
    def test_token_refresh_request_valid(self):
        """Test TokenRefreshRequest model"""
        refresh_data = {
            "refresh_token": "refresh.token.here"
        }
        
        refresh_request = TokenRefreshRequest(**refresh_data)
        
        assert refresh_request.refresh_token == refresh_data["refresh_token"]
    
    def test_token_response_valid(self):
        """Test TokenResponse model"""
        token_data = {
            "access_token": "new.access.token",
            "expires_in": 900
        }
        
        token_response = TokenResponse(**token_data)
        
        assert token_response.access_token == token_data["access_token"]
        assert token_response.token_type == "bearer"  # Default value
        assert token_response.expires_in == token_data["expires_in"]
    
    def test_token_payload_valid(self):
        """Test TokenPayload model"""
        now = datetime.utcnow()
        payload_data = {
            "sub": "user123",
            "username": "testuser",
            "email": "test@example.com",
            "is_admin": False,
            "exp": now,
            "iat": now
        }
        
        token_payload = TokenPayload(**payload_data)
        
        assert token_payload.sub == payload_data["sub"]
        assert token_payload.username == payload_data["username"]
        assert token_payload.email == payload_data["email"]
        assert token_payload.is_admin == payload_data["is_admin"]
        assert token_payload.exp == payload_data["exp"]
        assert token_payload.iat == payload_data["iat"]
    
    def test_token_payload_defaults(self):
        """Test TokenPayload model default values"""
        now = datetime.utcnow()
        payload_data = {
            "sub": "user123",
            "username": "testuser",
            "email": "test@example.com",
            "exp": now,
            "iat": now
        }
        
        token_payload = TokenPayload(**payload_data)
        
        # Test default
        assert token_payload.is_admin == False
    
    def test_model_serialization(self):
        """Test that models can be serialized to JSON"""
        user_data = {
            "id": "user123",
            "username": "testuser",
            "email": "test@example.com",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        user = User(**user_data)
        
        # Should be able to serialize to dict
        user_dict = user.dict()
        assert isinstance(user_dict, dict)
        assert user_dict["id"] == user_data["id"]
        
        # Should be able to serialize to JSON
        user_json = user.json()
        assert isinstance(user_json, str)
        assert user_data["id"] in user_json
