from app.services.travel.state import TravelState


def run(state: TravelState) -> TravelState:
    assumptions = list(state.get("assumptions", []))
    if not state["interests"]:
        assumptions.append("No interests provided; defaulted to local highlights.")
    if state["days"] <= 2:
        assumptions.append("Short trip detected; itinerary kept compact.")
    return {
        **state,
        "assumptions": assumptions,
    }
