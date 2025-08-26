import pytest
from httpx import AsyncClient, ASGITransport

from src.api.main import app, get_current_username


# ✅ Always bypass auth in tests
@pytest.fixture(autouse=True)
def bypass_auth():
    app.dependency_overrides[get_current_username] = lambda: "testuser"
    yield
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_health_check():
    """Simple test to ensure /health endpoint works"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
