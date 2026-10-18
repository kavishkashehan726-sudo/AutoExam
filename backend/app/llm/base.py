"""Pluggable LLM provider interface.

Every provider returns raw JSON text for generation; callers validate it with Pydantic.
"""

from typing import Protocol


class LLMProvider(Protocol):
    name: str
    model: str

    def generate_json(self, prompt: str, *, system: str | None = None) -> str:
        """Return the model's response as a JSON string."""
        ...

    def embed(self, texts: list[str]) -> list[list[float]]:
        """Return one embedding vector per input text."""
        ...
