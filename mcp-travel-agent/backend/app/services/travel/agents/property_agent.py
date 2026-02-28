from app.services.travel.state import TravelState
from app.services.travel.tools.airbnb_tools import AirbnbTools


class PropertyAgent:
    def __init__(self, tools: AirbnbTools) -> None:
        self.tools = tools

    def run(self, state: TravelState) -> TravelState:
        properties = self.tools.search_properties(
            destination=state["selected_destination"],
            days=state["days"],
            travelers=state["travelers"],
            budget_usd=state["budget_usd"],
            interests=state["interests"],
        )
        return {
            **state,
            "property_candidates": properties,
        }
