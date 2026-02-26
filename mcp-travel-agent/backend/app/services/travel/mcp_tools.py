class MCPTravelTools:
    """Mock MCP tools for flights/hotels/city guides.

    Replace these methods with real MCP client calls when your MCP servers are available.
    """

    def search_flights(self, origin: str, destination: str, budget_usd: int) -> list[dict[str, str | int]]:
        base = max(180, int(budget_usd * 0.25))
        return [
            {"airline": "SkyWays", "route": f"{origin} -> {destination}", "estimated_price_usd": base},
            {"airline": "AeroBlue", "route": f"{origin} -> {destination}", "estimated_price_usd": base + 70},
        ]

    def search_hotels(self, destination: str, budget_usd: int, days: int) -> list[dict[str, str | int]]:
        per_night = max(80, int((budget_usd * 0.45) / max(days, 1)))
        return [
            {
                "name": f"Central Stay {destination}",
                "area": "City Center",
                "estimated_price_per_night_usd": per_night,
            },
            {
                "name": f"Budget Inn {destination}",
                "area": "Transit District",
                "estimated_price_per_night_usd": max(60, per_night - 35),
            },
        ]

    def city_guide(self, destination: str, interests: list[str], days: int) -> list[dict[str, int | str]]:
        base_interest = interests[0] if interests else "local highlights"
        itinerary: list[dict[str, int | str]] = []
        for day in range(1, days + 1):
            itinerary.append(
                {
                    "day": day,
                    "plan": f"Explore {destination} focusing on {base_interest}; include one food and one neighborhood stop.",
                }
            )
        return itinerary
