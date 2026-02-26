from app.api.schemas.travel import TravelPlanRequest
from app.services.travel import state as state_types
from app.services.travel.agents import (
    destination_agent,
    flights_agent,
    hotels_agent,
    intake_agent,
    itinerary_agent,
    summary_agent,
)
from app.services.travel.mcp_tools import MCPTravelTools


class TravelWorkflowService:
    """Coordinates a multi-agent travel planning workflow.

    Plain English:
    - Intake agent captures assumptions.
    - Destination agent chooses likely places.
    - Flights/hotels/itinerary agents call MCP-like tools.
    - Summary agent creates the final user-facing plan summary.
    """

    def __init__(self) -> None:
        self._tools = MCPTravelTools()
        self._graph = self._build_graph()

    def _build_graph(self):
        try:
            from langgraph.graph import END, START, StateGraph
        except ImportError:
            return None

        graph = StateGraph(state_types.TravelState)
        graph.add_node("intake_agent", self._intake_node)
        graph.add_node("destination_agent", self._destination_node)
        graph.add_node("flights_agent", self._flights_node)
        graph.add_node("hotels_agent", self._hotels_node)
        graph.add_node("itinerary_agent", self._itinerary_node)
        graph.add_node("summary_agent", self._summary_node)

        graph.add_edge(START, "intake_agent")
        graph.add_edge("intake_agent", "destination_agent")
        graph.add_edge("destination_agent", "flights_agent")
        graph.add_edge("flights_agent", "hotels_agent")
        graph.add_edge("hotels_agent", "itinerary_agent")
        graph.add_edge("itinerary_agent", "summary_agent")
        graph.add_edge("summary_agent", END)

        return graph.compile()

    def plan(self, request: TravelPlanRequest) -> dict:
        state: state_types.TravelState = {
            "query": request.query,
            "origin": request.origin,
            "days": request.days,
            "budget_usd": request.budget_usd,
            "travelers": request.travelers,
            "interests": request.interests,
            "destination_options": [],
            "selected_destination": "",
            "flight_options": [],
            "hotel_options": [],
            "itinerary": [],
            "assumptions": [],
            "summary": "",
        }

        if self._graph is not None:
            output = self._graph.invoke(state)
        else:
            # Fallback mode when langgraph package is unavailable.
            output = self._run_sequential(state)

        return {
            "summary": output["summary"],
            "selected_destination": output["selected_destination"],
            "destination_options": output["destination_options"],
            "flight_options": output["flight_options"],
            "hotel_options": output["hotel_options"],
            "itinerary": output["itinerary"],
            "assumptions": output["assumptions"],
        }

    def _run_sequential(self, state: state_types.TravelState) -> state_types.TravelState:
        state = self._intake_node(state)
        state = self._destination_node(state)
        state = self._flights_node(state)
        state = self._hotels_node(state)
        state = self._itinerary_node(state)
        state = self._summary_node(state)
        return state

    def _intake_node(self, state: state_types.TravelState) -> state_types.TravelState:
        return intake_agent.run(state)

    def _destination_node(self, state: state_types.TravelState) -> state_types.TravelState:
        return destination_agent.run(state)

    def _flights_node(self, state: state_types.TravelState) -> state_types.TravelState:
        return flights_agent.run(state, self._tools)

    def _hotels_node(self, state: state_types.TravelState) -> state_types.TravelState:
        return hotels_agent.run(state, self._tools)

    def _itinerary_node(self, state: state_types.TravelState) -> state_types.TravelState:
        return itinerary_agent.run(state, self._tools)

    def _summary_node(self, state: state_types.TravelState) -> state_types.TravelState:
        return summary_agent.run(state)
