import pytest
from fastapi.testclient import TestClient
from mcp_server.server import app
from mcp_server.models import Message, ChatRequest

@pytest.fixture
def client():
    return TestClient(app)

def test_chat_completion_success(client, monkeypatch):
    test_response = {"message": {"content": "Test response"}}
    
    async def mock_post(*args, **kwargs):
        class MockResponse:
            def raise_for_status(self):
                pass
            def json(self):
                return test_response
        return MockResponse()

    with monkeypatch.context() as m:
        m.setattr("httpx.AsyncClient.post", mock_post)
        response = client.post(
            "/v1/chat/completions",
            json={
                "messages": [{"role": "user", "content": "Hello"}],
                "temperature": 0.7
            }
        )
    
    assert response.status_code == 200
    assert response.json() == {"content": "Test response"}

def test_chat_completion_error(client, monkeypatch):
    async def mock_post(*args, **kwargs):
        raise httpx.HTTPError("Test error")

    with monkeypatch.context() as m:
        m.setattr("httpx.AsyncClient.post", mock_post)
        response = client.post(
            "/v1/chat/completions",
            json={
                "messages": [{"role": "user", "content": "Hello"}],
                "temperature": 0.7
            }
        )
    
    assert response.status_code == 500
    assert "Test error" in response.json()["detail"]

def test_chat_request_validation(client):
    response = client.post(
        "/v1/chat/completions",
        json={
            "messages": [],  # Empty messages array should fail validation
            "temperature": 0.7
        }
    )
    assert response.status_code == 422