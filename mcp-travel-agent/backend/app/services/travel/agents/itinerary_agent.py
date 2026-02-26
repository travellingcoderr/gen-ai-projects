from app.services.travel.mcp_tools import MCPTravelTools
from app.services.travel.state import TravelState


def run(state: TravelState, tools: MCPTravelTools) -> TravelState:
    itinerary = tools.city_guide(
        destination=state["selected_destination"],
        interests=state["interests"],
        days=state["days"],
    )
    return {
        **state,
        "itinerary": itinerary,
    }
