"""Gemini implementation of LLMProvider using Gemini generateContent streaming."""
from typing import Any, Iterator

import google.generativeai as genai

from app.core.config import settings
from app.services.llm.base import LLMChatStream, StreamEvent


class _GeminiStreamAdapter:
    def __init__(self, gemini_stream: Any) -> None:
        self._stream = gemini_stream

    def __enter__(self) -> "_GeminiStreamAdapter":
        return self

    def __exit__(self, *args: object) -> None:
        return None

    def __iter__(self) -> Iterator[StreamEvent]:
        for chunk in self._stream:
            if hasattr(chunk, "text") and chunk.text:
                yield StreamEvent(kind="delta", text=chunk.text)

        yield StreamEvent(kind="done", response_id="gemini-stream")


class GeminiProvider:
    def __init__(self) -> None:
        api_key = getattr(settings, "GEMINI_API_KEY", "")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not set in environment variables")
        genai.configure(api_key=api_key)

    def stream_chat(
        self,
        model: str,
        input_items: list[dict[str, Any]],
        previous_response_id: str | None = None,
    ) -> LLMChatStream:
        del previous_response_id

        system_instruction = None
        messages: list[dict[str, Any]] = []
        for item in input_items:
            role = item.get("role", "")
            content = item.get("content", "")
            if role == "system":
                system_instruction = content
            elif role in ("user", "assistant"):
                messages.append({"role": role, "parts": [content]})

        model_name = model or settings.resolved_llm_model()
        gemini_model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=system_instruction,
        )

        chat = gemini_model.start_chat(history=messages[:-1] if len(messages) > 1 else [])
        last_message = messages[-1]["parts"][0] if messages else ""
        response = chat.send_message(last_message, stream=True)
        return _GeminiStreamAdapter(response)
