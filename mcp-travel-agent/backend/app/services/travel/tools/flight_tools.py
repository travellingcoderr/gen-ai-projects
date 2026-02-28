from app.services.travel.tools.mcp_connector import MCPConnector


class FlightTools:
    def __init__(self, connector: MCPConnector) -> None:
        self.connector = connector

    def search_flights(self, origin: str, destination: str, budget_usd: int) -> list[dict[str, object]]:
        self.connector.call_tool(
            server_name="expedia",
            tool_name="search_flights",
            payload={
                "origin": origin,
                "destination": destination,
                "budget_usd": budget_usd,
            },
        )

        base = max(180, int(budget_usd * 0.25))
        return [
            {
                "carrier": "SkyWays",
                "route": f"{origin} -> {destination}",
                "estimated_price_usd": base,
                "notes": "Morning departure, one checked bag not included.",
            },
            {
                "carrier": "AeroBlue",
                "route": f"{origin} -> {destination}",
                "estimated_price_usd": base + 60,
                "notes": "Later departure, more flexible timing.",
            },
        ]
