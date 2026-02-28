from app.services.travel.state import TravelState
from app.services.travel.tools.flight_tools import FlightTools


class FlightAgent:
    def __init__(self, tools: FlightTools) -> None:
        self.tools = tools

    def run(self, state: TravelState) -> TravelState:
        flights = self.tools.search_flights(
            origin=state["origin"],
            destination=state["selected_destination"],
            budget_usd=state["budget_usd"],
        )
        return {
            **state,
            "flight_options": flights,
        }
