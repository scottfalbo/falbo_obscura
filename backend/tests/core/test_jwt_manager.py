import pytest
from datetime import datetime, timedelta
from unittest.mock import patch
from shared.utils.jwt_manager import JWTManager
from core.models.auth import User


@pytest.fixture
def jwt_manager():
    """JWT manager instance for testing"""
    return JWTManager()


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
def admin_user():
    """Sample admin user for testing"""
    return User(
        id="admin123",
        username="admin",
        email="admin@example.com",
        is_active=True,
        is_admin=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )


@pytest.mark.unit
class TestJWTManager:
    
    def test_create_access_token(self, jwt_manager, sample_user):
        """Test access token creation contains correct payload"""
        token = jwt_manager.create_access_token(sample_user)
        
        assert isinstance(token, str)
        assert len(token) > 0
        
        # Verify token payload
        payload = jwt_manager.verify_token(token)
        assert payload is not None
        assert payload.sub == sample_user.id
        assert payload.username == sample_user.username
        assert payload.email == sample_user.email
        assert payload.is_admin == sample_user.is_admin
    
    def test_create_refresh_token(self, jwt_manager, sample_user):
        """Test refresh token creation"""
        token = jwt_manager.create_refresh_token(sample_user)
        
        assert isinstance(token, str)
        assert len(token) > 0
        
        # Verify token payload
        payload = jwt_manager.verify_token(token)
        assert payload is not None
        assert payload.sub == sample_user.id
        assert payload.username == sample_user.username
    
    def test_verify_valid_token(self, jwt_manager, sample_user):
        """Test token verification with valid token"""
        token = jwt_manager.create_access_token(sample_user)
        payload = jwt_manager.verify_token(token)
        
        assert payload is not None
        assert payload.sub == sample_user.id
        assert payload.username == sample_user.username
        assert payload.email == sample_user.email
    
    def test_verify_invalid_token(self, jwt_manager):
        """Test token verification with invalid token"""
        invalid_token = "invalid.jwt.token"
        payload = jwt_manager.verify_token(invalid_token)
        
        assert payload is None
    
    def test_verify_expired_token(self, jwt_manager, sample_user):
        """Test token verification with expired token"""
        # Mock expired time
        with patch('shared.utils.jwt_manager.datetime') as mock_datetime:
            # Set current time to past
            past_time = datetime.utcnow() - timedelta(hours=1)
            mock_datetime.utcnow.return_value = past_time
            mock_datetime.fromtimestamp = datetime.fromtimestamp
            
            # Create token in the past
            token = jwt_manager.create_access_token(sample_user)
        
        # Verify token is now expired
        payload = jwt_manager.verify_token(token)
        assert payload is None
    
    def test_admin_token_creation(self, jwt_manager, admin_user):
        """Test token creation for admin user"""
        token = jwt_manager.create_access_token(admin_user)
        payload = jwt_manager.verify_token(token)
        
        assert payload is not None
        assert payload.is_admin == True
    
    def test_password_hashing(self, jwt_manager):
        """Test password hashing and verification"""
        password = "test_password_123"
        
        # Hash password
        hashed = jwt_manager.hash_password(password)
        assert isinstance(hashed, str)
        assert hashed != password  # Should be different from original
        assert len(hashed) > 20  # Bcrypt hashes are long
        
        # Verify correct password
        assert jwt_manager.verify_password(password, hashed) == True
        
        # Verify incorrect password
        assert jwt_manager.verify_password("wrong_password", hashed) == False
    
    def test_password_hash_uniqueness(self, jwt_manager):
        """Test that same password generates different hashes (salt)"""
        password = "same_password"
        
        hash1 = jwt_manager.hash_password(password)
        hash2 = jwt_manager.hash_password(password)
        
        # Hashes should be different due to salt
        assert hash1 != hash2
        
        # But both should verify the same password
        assert jwt_manager.verify_password(password, hash1) == True
        assert jwt_manager.verify_password(password, hash2) == True
