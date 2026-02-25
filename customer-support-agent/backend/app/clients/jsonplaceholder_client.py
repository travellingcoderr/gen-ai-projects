import httpx


class JsonPlaceholderClient:
    base_url = "https://jsonplaceholder.typicode.com"

    def list_posts(self) -> list[dict]:
        with httpx.Client(timeout=10.0) as client:
            response = client.get(f"{self.base_url}/posts")
            response.raise_for_status()
            data = response.json()

        return data[:10]
