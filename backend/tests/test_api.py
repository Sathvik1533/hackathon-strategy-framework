import pytest

@pytest.mark.asyncio
async def test_health_endpoint(async_client):
    response = await async_client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "api_status" in data["data"]

@pytest.mark.asyncio
async def test_auth_login(async_client):
    response = await async_client.post(
        "/api/v1/auth/login",
        json={"email": "developer@hackathon.dev", "password": "secure_password"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "access_token" in data["data"]
