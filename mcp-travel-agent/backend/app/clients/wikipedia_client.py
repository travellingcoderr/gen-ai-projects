from typing import Any

import httpx


class WikipediaClient:
    base_url = "https://en.wikipedia.org/w/api.php"

    async def search(self, query: str) -> list[dict[str, str]]:
        params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": query,
            "srlimit": 5,
        }
        headers = {"User-Agent": "mcp-travel-agent/1.0 (https://github.com/your-org/mcp-travel-agent)"}
        async with httpx.AsyncClient(timeout=10.0, headers=headers) as client:
            response = await client.get(self.base_url, params=params)
            response.raise_for_status()
            payload: dict[str, Any] = response.json()

        items = payload.get("query", {}).get("search", [])
        return [
            {
                "title": item.get("title", ""),
                "url": f"https://en.wikipedia.org/wiki/{item.get('title', '').replace(' ', '_')}",
                "source": "wikipedia",
            }
            for item in items
        ]
