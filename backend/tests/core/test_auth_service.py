import pytest
from unittest.mock import AsyncMock, Mock
from datetime import datetime
from core.services.auth_service import AuthService
from core.models.auth import User, LoginRequest, LoginResponse, TokenResponse
from core.interfaces.auth_repository import IAuthRepository


@pytest.fixture
def mock_auth_repository():
    """Mock auth repository for testing"""
    return AsyncMock(spec=IAuthRepository)


@pytest.fixture
def auth_service(mock_auth_repository):
    """Auth service with mocked repository"""
    return AuthService(mock_auth_repository)


@pytest.fixture
def sample_user():
    """Sample user for testing"""
    return User(
        id="user123",
        username="testuser",
        email="test@example.com",
        is_active=True,
        is_admin=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )


@pytest.fixture
def login_request():
    """Sample login request"""
    return LoginRequest(username="testuser", password="password123")


@pytest.mark.unit
class TestAuthService:
    
    async def test_successful_login(self, auth_service, mock_auth_repository, login_request, sample_user):
        """Test successful user login returns tokens and user info"""
        # Setup mock
        mock_auth_repository.authenticate_user.return_value = sample_user
        
        # Execute
        result = await auth_service.login(login_request)
        
        # Verify
        assert result is not None
        assert isinstance(result, LoginResponse)
        assert result.user.id == sample_user.id
        assert result.user.username == sample_user.username
        assert result.access_token is not None
        assert result.refresh_token is not None
        assert result.token_type == "bearer"
        assert result.expires_in > 0
        
        # Verify repository was called
        mock_auth_repository.authenticate_user.assert_called_once_with(login_request)
    
    async def test_failed_login(self, auth_service, mock_auth_repository, login_request):
        """Test failed login with invalid credentials"""
        # Setup mock to return None (authentication failed)
        mock_auth_repository.authenticate_user.return_value = None
        
        # Execute
        result = await auth_service.login(login_request)
        
        # Verify
        assert result is None
        mock_auth_repository.authenticate_user.assert_called_once_with(login_request)
    
    async def test_successful_token_refresh(self, auth_service, mock_auth_repository, sample_user):
        """Test successful token refresh"""
        # Create a valid refresh token
        from shared.utils.jwt_manager import jwt_manager
        refresh_token = jwt_manager.create_refresh_token(sample_user)
        
        # Setup mock
        mock_auth_repository.get_user_by_id.return_value = sample_user
        
        # Execute
        result = await auth_service.refresh_token(refresh_token)
        
        # Verify
        assert result is not None
        assert isinstance(result, TokenResponse)
        assert result.access_token is not None
        assert result.token_type == "bearer"
        assert result.expires_in > 0
        
        # Verify repository was called with correct user ID
        mock_auth_repository.get_user_by_id.assert_called_once_with(sample_user.id)
    
    async def test_failed_token_refresh_invalid_token(self, auth_service, mock_auth_repository):
        """Test token refresh with invalid refresh token"""
        invalid_token = "invalid.token.here"
        
        # Execute
        result = await auth_service.refresh_token(invalid_token)
        
        # Verify
        assert result is None
        # Repository should not be called for invalid token
        mock_auth_repository.get_user_by_id.assert_not_called()
    
    async def test_failed_token_refresh_user_not_found(self, auth_service, mock_auth_repository, sample_user):
        """Test token refresh when user no longer exists"""
        # Create a valid refresh token
        from shared.utils.jwt_manager import jwt_manager
        refresh_token = jwt_manager.create_refresh_token(sample_user)
        
        # Setup mock to return None (user not found)
        mock_auth_repository.get_user_by_id.return_value = None
        
        # Execute
        result = await auth_service.refresh_token(refresh_token)
        
        # Verify
        assert result is None
        mock_auth_repository.get_user_by_id.assert_called_once_with(sample_user.id)
    
    async def test_get_current_user_valid_token(self, auth_service, mock_auth_repository, sample_user):
        """Test getting current user with valid token"""
        # Create a valid access token
        from shared.utils.jwt_manager import jwt_manager
        access_token = jwt_manager.create_access_token(sample_user)
        
        # Setup mock
        mock_auth_repository.get_user_by_id.return_value = sample_user
        
        # Execute
        result = await auth_service.get_current_user(access_token)
        
        # Verify
        assert result is not None
        assert result.id == sample_user.id
        assert result.username == sample_user.username
        mock_auth_repository.get_user_by_id.assert_called_once_with(sample_user.id)
    
    async def test_get_current_user_invalid_token(self, auth_service, mock_auth_repository):
        """Test getting current user with invalid token"""
        invalid_token = "invalid.token.here"
        
        # Execute
        result = await auth_service.get_current_user(invalid_token)
        
        # Verify
        assert result is None
        # Repository should not be called for invalid token
        mock_auth_repository.get_user_by_id.assert_not_called()
    
    async def test_create_user(self, auth_service, mock_auth_repository, sample_user):
        """Test user creation"""
        username = "newuser"
        email = "new@example.com"
        password = "password123"
        
        # Setup mock
        mock_auth_repository.create_user.return_value = sample_user
        
        # Execute
        result = await auth_service.create_user(username, email, password)
        
        # Verify
        assert result is not None
        assert result.id == sample_user.id
        mock_auth_repository.create_user.assert_called_once_with(username, email, password)
