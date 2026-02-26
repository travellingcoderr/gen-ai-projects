from pydantic import BaseModel


class LLMConfigResponse(BaseModel):
    provider: str
    model: str
    has_openai_key: bool
    has_gemini_key: bool
