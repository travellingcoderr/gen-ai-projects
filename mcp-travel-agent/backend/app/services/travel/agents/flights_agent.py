from app.services.travel.mcp_tools import MCPTravelTools
from app.services.travel.state import TravelState


def run(state: TravelState, tools: MCPTravelTools) -> TravelState:
    flights = tools.search_flights(
        origin=state["origin"],
        destination=state["selected_destination"],
        budget_usd=state["budget_usd"],
    )
    return {
        **state,
        "flight_options": flights,
    }
