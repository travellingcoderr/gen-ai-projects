from fastapi.testclient import TestClient

from app.main import app


def test_langgraph_support_flow() -> None:
    client = TestClient(app)
    response = client.post("/api/langgraph/support", json={"query": "I need a refund for a double charge"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["category"] == "billing"
    assert payload["response"].strip()
    assert payload["query"] == "I need a refund for a double charge"


def test_langgraph_support_technical_category() -> None:
    client = TestClient(app)
    response = client.post("/api/langgraph/support", json={"query": "The app keeps crashing with an error"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["category"] == "technical"


def test_langgraph_support_accepts_legacy_message_field() -> None:
    client = TestClient(app)
    response = client.post("/api/langgraph/support", json={"message": "where is my invoice"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["category"] == "billing"
    assert payload["query"] == "where is my invoice"
