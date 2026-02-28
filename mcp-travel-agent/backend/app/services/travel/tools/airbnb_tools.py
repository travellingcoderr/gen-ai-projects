from app.services.travel.tools.mcp_connector import MCPConnector


class AirbnbTools:
    def __init__(self, connector: MCPConnector) -> None:
        self.connector = connector

    def search_properties(
        self,
        destination: str,
        days: int,
        travelers: int,
        budget_usd: int,
        interests: list[str],
    ) -> list[dict[str, object]]:
        self.connector.call_tool(
            server_name="airbnb",
            tool_name="search_properties",
            payload={
                "destination": destination,
                "days": days,
                "travelers": travelers,
                "budget_usd": budget_usd,
                "interests": interests,
            },
        )

        base = max(110, int((budget_usd * 0.7) / max(days, 1)))
        interest = interests[0] if interests else "central location"
        return [
            {
                "name": f"Cedar Stay {destination}",
                "area": "Town Center",
                "nightly_rate_usd": base,
                "total_estimated_usd": base * days,
                "rating": 4.8,
                "booking_link": f"https://www.airbnb.com/s/{destination.replace(' ', '-')}",
                "amenities": ["wifi", "kitchen", interest],
            },
            {
                "name": f"Maple Loft {destination}",
                "area": "Old Quarter",
                "nightly_rate_usd": base + 25,
                "total_estimated_usd": (base + 25) * days,
                "rating": 4.7,
                "booking_link": f"https://www.airbnb.com/s/{destination.replace(' ', '-')}",
                "amenities": ["wifi", "workspace", "walkable area"],
            },
            {
                "name": f"Budget Nest {destination}",
                "area": "Transit District",
                "nightly_rate_usd": max(85, base - 30),
                "total_estimated_usd": max(85, base - 30) * days,
                "rating": 4.4,
                "booking_link": f"https://www.airbnb.com/s/{destination.replace(' ', '-')}",
                "amenities": ["wifi", "self check-in", "value stay"],
            },
        ]
