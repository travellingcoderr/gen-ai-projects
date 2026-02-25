from app.api.schemas.llm import LLMConfigResponse
from app.services.llm_service import LLMService


class LLMOrchestrator:
    def __init__(self, llm_service: LLMService) -> None:
        self.llm_service = llm_service

    def config(self) -> LLMConfigResponse:
        data = self.llm_service.get_runtime_config()
        return LLMConfigResponse(**data)
