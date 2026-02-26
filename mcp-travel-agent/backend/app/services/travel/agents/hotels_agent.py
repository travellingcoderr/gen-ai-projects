from app.services.travel.mcp_tools import MCPTravelTools
from app.services.travel.state import TravelState


def run(state: TravelState, tools: MCPTravelTools) -> TravelState:
    hotels = tools.search_hotels(
        destination=state["selected_destination"],
        budget_usd=state["budget_usd"],
        days=state["days"],
    )
    return {
        **state,
        "hotel_options": hotels,
    }
