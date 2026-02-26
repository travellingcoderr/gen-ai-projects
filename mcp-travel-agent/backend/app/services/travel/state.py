from typing import TypedDict


class TravelState(TypedDict):
    query: str
    origin: str
    days: int
    budget_usd: int
    travelers: int
    interests: list[str]
    destination_options: list[dict[str, str]]
    selected_destination: str
    flight_options: list[dict[str, str | int]]
    hotel_options: list[dict[str, str | int]]
    itinerary: list[dict[str, int | str]]
    assumptions: list[str]
    summary: str
