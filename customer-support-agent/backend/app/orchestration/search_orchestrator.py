from app.api.schemas.search import SearchResponse, SearchResult
from app.services.search_service import SearchService


class SearchOrchestrator:
    def __init__(self, search_service: SearchService) -> None:
        self.search_service = search_service

    async def search(self, query: str) -> SearchResponse:
        results = await self.search_service.search(query)
        return SearchResponse(
            query=query,
            results=[SearchResult(**item) for item in results],
        )
