from pydantic import BaseModel, Field


class TravelPlanRequest(BaseModel):
    query: str = Field(..., min_length=3)
    origin: str = Field(default="New York")
    days: int = Field(default=4, ge=1, le=14)
    budget_usd: int = Field(default=2000, ge=200)
    travelers: int = Field(default=1, ge=1, le=10)
    interests: list[str] = Field(default_factory=list)


class DestinationOption(BaseModel):
    city: str
    why: str


class FlightOption(BaseModel):
    airline: str
    route: str
    estimated_price_usd: int


class HotelOption(BaseModel):
    name: str
    area: str
    estimated_price_per_night_usd: int


class ItineraryDay(BaseModel):
    day: int
    plan: str


class TravelPlanResponse(BaseModel):
    summary: str
    selected_destination: str
    destination_options: list[DestinationOption]
    flight_options: list[FlightOption]
    hotel_options: list[HotelOption]
    itinerary: list[ItineraryDay]
    assumptions: list[str]
