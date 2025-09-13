import pytest
from fastapi.testclient import TestClient


@pytest.mark.unit
def test_root_endpoint(client):
    """Test the root endpoint returns expected message"""
    response = client.get("/")
    
    assert response.status_code == 200
    assert response.json() == {"message": "Falbo Obscura API is running"}


@pytest.mark.unit
def test_health_check_endpoint(client):
    """Test the health check endpoint"""
    response = client.get("/health")
    
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


@pytest.mark.integration
async def test_root_endpoint_async(async_client):
    """Test the root endpoint with async client"""
    response = await async_client.get("/")
    
    assert response.status_code == 200
    assert response.json() == {"message": "Falbo Obscura API is running"}
