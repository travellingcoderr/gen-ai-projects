from app.clients.jsonplaceholder_client import JsonPlaceholderClient
from app.clients.wikipedia_client import WikipediaClient
from app.orchestration.jsonplaceholder_orchestrator import JsonPlaceholderOrchestrator
from app.orchestration.llm_orchestrator import LLMOrchestrator
from app.orchestration.search_orchestrator import SearchOrchestrator
from app.services.llm_service import LLMService
from app.services.search_service import SearchService


def get_wikipedia_client() -> WikipediaClient:
    return WikipediaClient()


def get_jsonplaceholder_client() -> JsonPlaceholderClient:
    return JsonPlaceholderClient()


def get_search_orchestrator() -> SearchOrchestrator:
    service = SearchService(wikipedia_client=get_wikipedia_client())
    return SearchOrchestrator(search_service=service)


def get_jsonplaceholder_orchestrator() -> JsonPlaceholderOrchestrator:
    return JsonPlaceholderOrchestrator(client=get_jsonplaceholder_client())


def get_llm_orchestrator() -> LLMOrchestrator:
    return LLMOrchestrator(llm_service=LLMService())
