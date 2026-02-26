from app.api.schemas.langgraph import LangGraphSupportResponse
from app.services.langgraph_support_service import LangGraphSupportService


class LangGraphOrchestrator:
    def __init__(self, service: LangGraphSupportService) -> None:
        self.service = service

    def process_support_message(self, query: str) -> LangGraphSupportResponse:
        payload = self.service.run(query)
        return LangGraphSupportResponse(**payload)
