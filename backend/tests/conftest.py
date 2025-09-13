import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from main import app


@pytest.fixture
def client():
    """Synchronous test client for FastAPI app"""
    with TestClient(app) as c:
        yield c


@pytest.fixture
async def async_client():
    """Asynchronous test client for FastAPI app"""
    from httpx import ASGITransport
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture
def sample_gallery_data():
    """Sample gallery data for testing"""
    return {
        "title": "Test Gallery",
        "description": "A test gallery",
        "category": "tattoo",
        "images": [
            {"url": "https://example.com/image1.jpg", "caption": "Test image 1"},
            {"url": "https://example.com/image2.jpg", "caption": "Test image 2"}
        ]
    }


@pytest.fixture
def sample_user_data():
    """Sample user data for testing"""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123"
    }
