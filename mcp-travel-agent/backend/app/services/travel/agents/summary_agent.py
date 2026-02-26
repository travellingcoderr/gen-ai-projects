from app.services.travel.state import TravelState


def run(state: TravelState) -> TravelState:
    summary = (
        f"Planned a {state['days']}-day trip to {state['selected_destination']} for "
        f"{state['travelers']} traveler(s), starting from {state['origin']}, within about ${state['budget_usd']}."
    )
    return {
        **state,
        "summary": summary,
    }
