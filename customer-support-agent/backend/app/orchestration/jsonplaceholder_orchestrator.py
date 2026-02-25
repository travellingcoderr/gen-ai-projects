from app.clients.jsonplaceholder_client import JsonPlaceholderClient


class JsonPlaceholderOrchestrator:
    def __init__(self, client: JsonPlaceholderClient) -> None:
        self.client = client

    def list_posts(self) -> list[dict]:
        return self.client.list_posts()
