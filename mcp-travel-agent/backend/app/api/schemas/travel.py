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
    carrier: str
    route: str
    estimated_price_usd: int
    notes: str


class ParsedRequirements(BaseModel):
    destination: str
    origin: str
    days: int
    budget_usd: int
    travelers: int
    interests: list[str]
    notes: str


class PropertyOption(BaseModel):
    name: str
    area: str
    nightly_rate_usd: int
    total_estimated_usd: int
    rating: float
    booking_link: str
    match_score: float
    pros: list[str]
    cons: list[str]


class TravelPlanResponse(BaseModel):
    summary: str
    selected_destination: str
    parsed_requirements: ParsedRequirements
    top_properties: list[PropertyOption]
    flight_options: list[FlightOption]
    assumptions: list[str]
