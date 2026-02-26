"""
LLM abstraction: interface that any chat provider must implement.
This is the interface in the factory pattern.
"""
from dataclasses import dataclass
from typing import Iterator, Protocol, runtime_checkable


@dataclass
class StreamEvent:
    """Normalized event from any LLM stream."""

    kind: str  # "delta" | "done"
    text: str | None = None
    response_id: str | None = None


@runtime_checkable
class LLMChatStream(Protocol):
    """Context manager that yields normalized StreamEvent objects."""

    def __enter__(self) -> "LLMChatStream":
        ...

    def __exit__(self, *args: object) -> None:
        ...

    def __iter__(self) -> Iterator[StreamEvent]:
        ...


class LLMProvider(Protocol):
    """Interface for provider-specific streaming chat implementations."""

    def stream_chat(
        self,
        model: str,
        input_items: list[dict],
        previous_response_id: str | None = None,
    ) -> LLMChatStream:
        ...
