from fastapi.testclient import TestClient

from app.main import app


def test_llm_config_defaults() -> None:
    client = TestClient(app)
    response = client.get("/api/llm/config")
    assert response.status_code == 200
    payload = response.json()
    assert payload["provider"] == "openai"
    assert payload["model"] == "gpt-4o-mini"
