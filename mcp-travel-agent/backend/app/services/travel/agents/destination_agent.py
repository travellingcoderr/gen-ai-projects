from app.services.travel.state import TravelState


def _pick_by_interest(interests: list[str]) -> list[dict[str, str]]:
    text = " ".join(interests).lower()
    if any(word in text for word in ["beach", "island", "sun"]):
        return [
            {"city": "San Diego", "why": "Mild weather and easy beach access."},
            {"city": "Miami", "why": "Strong beach and nightlife options."},
            {"city": "Honolulu", "why": "Island-focused itinerary potential."},
        ]
    if any(word in text for word in ["history", "museum", "culture"]):
        return [
            {"city": "Washington, D.C.", "why": "High density of museums and landmarks."},
            {"city": "Boston", "why": "Strong historical trails and neighborhoods."},
            {"city": "Philadelphia", "why": "Compact historic core and food scene."},
        ]
    return [
        {"city": "Chicago", "why": "Balanced food, architecture, and neighborhoods."},
        {"city": "Austin", "why": "Strong live music and food options."},
        {"city": "Seattle", "why": "Urban + nature mix for flexible trips."},
    ]


def run(state: TravelState) -> TravelState:
    options = _pick_by_interest(state["interests"])
    selected = options[0]["city"]
    return {
        **state,
        "destination_options": options,
        "selected_destination": selected,
    }
