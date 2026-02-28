from app.api.schemas.travel import TravelPlanRequest
from app.services.travel import state as state_types
from app.services.travel.agents.analysis_agent import AnalysisAgent
from app.services.travel.agents.flight_agent import FlightAgent
from app.services.travel.agents.orchestrator_agent import OrchestratorAgent
from app.services.travel.agents.parser_agent import run as parse_request
from app.services.travel.agents.property_agent import PropertyAgent
from app.services.travel.tools.airbnb_tools import AirbnbTools
from app.services.travel.tools.flight_tools import FlightTools
from app.services.travel.tools.mcp_connector import MCPConnector


class TravelWorkflowService:
    """Reference-style multi-agent travel workflow.

    Layman version:
    - Parser agent figures out what the user wants.
    - Property agent fetches possible stays.
    - Flight agent fetches route options.
    - Analysis agent ranks the stays.
    - Orchestrator agent writes the final answer.

    The agent names mirror the reference project so the codebase is easier to compare and reason about.
    """

    def __init__(self) -> None:
        connector = MCPConnector()
        self._property_agent = PropertyAgent(AirbnbTools(connector))
        self._flight_agent = FlightAgent(FlightTools(connector))
        self._analysis_agent = AnalysisAgent()
        self._orchestrator_agent = OrchestratorAgent()
        self._graph = self._build_graph()

    def _build_graph(self):
        try:
            from langgraph.graph import END, START, StateGraph
        except ImportError:
            return None

        graph = StateGraph(state_types.TravelState)
        graph.add_node("parser_agent", self._parser_node)
        graph.add_node("property_agent", self._property_node)
        graph.add_node("flight_agent", self._flight_node)
        graph.add_node("analysis_agent", self._analysis_node)
        graph.add_node("orchestrator_agent", self._orchestrator_node)

        graph.add_edge(START, "parser_agent")
        graph.add_edge("parser_agent", "property_agent")
        graph.add_edge("property_agent", "flight_agent")
        graph.add_edge("flight_agent", "analysis_agent")
        graph.add_edge("analysis_agent", "orchestrator_agent")
        graph.add_edge("orchestrator_agent", END)
        return graph.compile()

    def plan(self, request: TravelPlanRequest) -> dict:
        state: state_types.TravelState = {
            "query": request.query,
            "origin": request.origin,
            "days": request.days,
            "budget_usd": request.budget_usd,
            "travelers": request.travelers,
            "interests": request.interests,
            "selected_destination": "",
            "parsed_requirements": {},
            "property_candidates": [],
            "top_properties": [],
            "flight_options": [],
            "assumptions": [],
            "summary": "",
        }

        output = self._graph.invoke(state) if self._graph is not None else self._run_sequential(state)
        return {
            "summary": output["summary"],
            "selected_destination": output["selected_destination"],
            "parsed_requirements": output["parsed_requirements"],
            "top_properties": output["top_properties"],
            "flight_options": output["flight_options"],
            "assumptions": output["assumptions"],
        }

    def _run_sequential(self, state: state_types.TravelState) -> state_types.TravelState:
        state = self._parser_node(state)
        state = self._property_node(state)
        state = self._flight_node(state)
        state = self._analysis_node(state)
        state = self._orchestrator_node(state)
        return state

    def _parser_node(self, state: state_types.TravelState) -> state_types.TravelState:
        return parse_request(state)

    def _property_node(self, state: state_types.TravelState) -> state_types.TravelState:
        return self._property_agent.run(state)

    def _flight_node(self, state: state_types.TravelState) -> state_types.TravelState:
        return self._flight_agent.run(state)

    def _analysis_node(self, state: state_types.TravelState) -> state_types.TravelState:
        return self._analysis_agent.run(state)

    def _orchestrator_node(self, state: state_types.TravelState) -> state_types.TravelState:
        return self._orchestrator_agent.run(state)
