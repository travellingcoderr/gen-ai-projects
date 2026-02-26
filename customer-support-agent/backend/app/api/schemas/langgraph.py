from pydantic import BaseModel, Field, model_validator


class LangGraphSupportRequest(BaseModel):
    query: str = Field(..., min_length=1)

    @model_validator(mode="before")
    @classmethod
    def _support_legacy_message(cls, data: object) -> object:
        if isinstance(data, dict) and "query" not in data and "message" in data:
            payload = dict(data)
            payload["query"] = payload["message"]
            return payload
        return data


class LangGraphSupportResponse(BaseModel):
    query: str
    category: str
    analysis: str
    response: str
