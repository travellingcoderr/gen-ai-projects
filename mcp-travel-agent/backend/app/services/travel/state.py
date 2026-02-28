from typing import TypedDict


class TravelState(TypedDict):
    query: str
    origin: str
    days: int
    budget_usd: int
    travelers: int
    interests: list[str]
    selected_destination: str
    parsed_requirements: dict[str, object]
    property_candidates: list[dict[str, object]]
    top_properties: list[dict[str, object]]
    flight_options: list[dict[str, object]]
    assumptions: list[str]
    summary: str
