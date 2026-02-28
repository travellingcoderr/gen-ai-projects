class MCPConnector:
    """Thin adapter boundary for future MCP server integration.

    Right now this class just documents the seam in the architecture.
    Later, replace `call_tool` with real MCP client logic and keep the rest of the agents unchanged.
    """

    def call_tool(self, server_name: str, tool_name: str, payload: dict) -> dict:
        return {
            "server": server_name,
            "tool": tool_name,
            "payload": payload,
        }
