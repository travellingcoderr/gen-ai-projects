from fastapi.testclient import TestClient

from app.main import app


def test_travel_plan_endpoint() -> None:
    client = TestClient(app)
    response = client.post(
        "/api/travel/plan",
        json={
            "query": "Plan a 4 day trip focused on beach food",
            "origin": "New York",
            "days": 4,
            "budget_usd": 2200,
            "travelers": 2,
            "interests": ["beach", "food"],
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["selected_destination"]
    assert len(payload["destination_options"]) >= 1
    assert len(payload["flight_options"]) >= 1
    assert len(payload["hotel_options"]) >= 1
    assert len(payload["itinerary"]) == 4
    assert payload["summary"]


def test_travel_plan_defaults() -> None:
    client = TestClient(app)
    response = client.post(
        "/api/travel/plan",
        json={
            "query": "Need a quick city break",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["selected_destination"]
    assert isinstance(payload["assumptions"], list)
