"""OpenAI implementation of LLMProvider using Responses API streaming."""
from typing import Any, Iterator

from openai import OpenAI

from app.core.config import settings
from app.services.llm.base import LLMChatStream, StreamEvent


class _OpenAIStreamAdapter:
    def __init__(self, openai_stream: Any) -> None:
        self._stream_manager = openai_stream
        self._stream: Any = None

    def __enter__(self) -> "_OpenAIStreamAdapter":
        self._stream = self._stream_manager.__enter__()
        return self

    def __exit__(self, *args: object) -> None:
        self._stream_manager.__exit__(*args)

    def __iter__(self) -> Iterator[StreamEvent]:
        if self._stream is None:
            raise RuntimeError("Stream not entered. Use 'with' statement.")
        for event in self._stream:
            if event.type == "response.output_text.delta":
                yield StreamEvent(kind="delta", text=event.delta or "")
            elif event.type == "response.completed" and getattr(event, "response", None):
                rid = getattr(event.response, "id", None) or ""
                yield StreamEvent(kind="done", response_id=rid)


class OpenAIProvider:
    def __init__(self) -> None:
        self._client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def stream_chat(
        self,
        model: str,
        input_items: list[dict[str, Any]],
        previous_response_id: str | None = None,
    ) -> LLMChatStream:
        raw = self._client.responses.stream(
            model=model,
            input=input_items,
            previous_response_id=previous_response_id,
        )
        return _OpenAIStreamAdapter(raw)
