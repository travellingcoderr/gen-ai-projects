import re

from app.services.travel.state import TravelState


_DESTINATIONS = {
    "coorg": "Coorg",
    "goa": "Goa",
    "tokyo": "Tokyo",
    "paris": "Paris",
    "seattle": "Seattle",
    "chicago": "Chicago",
    "san diego": "San Diego",
    "austin": "Austin",
}


def _extract_destination(query: str) -> str:
    lowered = query.lower()
    for key, value in _DESTINATIONS.items():
        if key in lowered:
            return value

    match = re.search(r"\bin\s+([A-Za-z][A-Za-z\s,.-]{1,40})", query)
    if match:
        candidate = match.group(1).strip(" .,")
        return candidate.title()
    return "Chicago"


def run(state: TravelState) -> TravelState:
    destination = _extract_destination(state["query"])
    assumptions = list(state.get("assumptions", []))
    if destination == "Chicago" and "chicago" not in state["query"].lower():
        assumptions.append("Destination not explicit in query; defaulted to Chicago.")
    if not state["interests"]:
        assumptions.append("No interests supplied; ranking for balanced city stay.")

    parsed_requirements = {
        "destination": destination,
        "origin": state["origin"],
        "days": state["days"],
        "budget_usd": state["budget_usd"],
        "travelers": state["travelers"],
        "interests": state["interests"],
        "notes": "Parsed from user query plus explicit request fields.",
    }

    return {
        **state,
        "selected_destination": destination,
        "parsed_requirements": parsed_requirements,
        "assumptions": assumptions,
    }
