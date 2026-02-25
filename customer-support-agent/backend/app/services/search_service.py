from app.clients.wikipedia_client import WikipediaClient


class SearchService:
    def __init__(self, wikipedia_client: WikipediaClient) -> None:
        self.wikipedia_client = wikipedia_client

    def search(self, query: str) -> list[dict[str, str]]:
        return self.wikipedia_client.search(query)
