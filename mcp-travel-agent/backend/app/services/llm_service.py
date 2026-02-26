from app.core.config import settings
from app.services.llm.factory import get_llm_provider


class LLMService:
    def get_runtime_config(self) -> dict[str, str | bool]:
        provider = (settings.LLM_PROVIDER or "openai").strip().lower()
        return {
            "provider": provider,
            "model": settings.resolved_llm_model(),
            "has_openai_key": bool(settings.OPENAI_API_KEY),
            "has_gemini_key": bool(settings.GEMINI_API_KEY),
        }

    def stream_chat(
        self,
        model: str,
        input_items: list[dict],
        previous_response_id: str | None = None,
    ):
        provider = get_llm_provider()
        return provider.stream_chat(
            model=model,
            input_items=input_items,
            previous_response_id=previous_response_id,
        )
