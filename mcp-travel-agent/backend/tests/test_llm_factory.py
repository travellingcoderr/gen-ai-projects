from app.core.config import settings
from app.services.llm.factory import get_llm_provider


def test_factory_selects_openai() -> None:
    previous = settings.LLM_PROVIDER
    settings.LLM_PROVIDER = "openai"
    try:
        provider = get_llm_provider()
        assert provider.__class__.__name__ == "OpenAIProvider"
    finally:
        settings.LLM_PROVIDER = previous


def test_factory_selects_gemini() -> None:
    previous = settings.LLM_PROVIDER
    settings.LLM_PROVIDER = "gemini"
    try:
        provider = get_llm_provider()
        assert provider.__class__.__name__ == "GeminiProvider"
    finally:
        settings.LLM_PROVIDER = previous
