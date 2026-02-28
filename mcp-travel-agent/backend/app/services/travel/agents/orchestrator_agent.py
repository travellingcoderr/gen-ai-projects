from app.services.travel.state import TravelState


class OrchestratorAgent:
    def run(self, state: TravelState) -> TravelState:
        property_count = len(state["top_properties"])
        cheapest_flight = min((int(item["estimated_price_usd"]) for item in state["flight_options"]), default=0)
        summary = (
            f"Found {property_count} ranked Airbnb-style properties in {state['selected_destination']} "
            f"for a {state['days']}-day trip. "
            f"Flights from {state['origin']} start around ${cheapest_flight}."
        )
        return {
            **state,
            "summary": summary,
        }
