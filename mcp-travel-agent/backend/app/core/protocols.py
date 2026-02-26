from typing import Protocol


class SearchClientProtocol(Protocol):
    def search(self, query: str) -> list[dict[str, str]]:
        ...
