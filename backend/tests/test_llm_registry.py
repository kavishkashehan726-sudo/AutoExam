import pytest

from app.core.config import Settings
from app.llm.registry import get_provider, register_provider


class FakeProvider:
    name = "fake"

    def __init__(self, settings: Settings) -> None:
        self.model = settings.llm_model

    def generate_json(self, prompt: str, *, system: str | None = None) -> str:
        return "{}"

    def embed(self, texts: list[str]) -> list[list[float]]:
        return [[0.0] for _ in texts]


def test_provider_and_model_come_from_settings() -> None:
    register_provider("fake", FakeProvider)
    provider = get_provider(Settings(llm_provider="fake", llm_model="some-model"))
    assert provider.name == "fake"
    assert provider.model == "some-model"


def test_unknown_provider_is_rejected() -> None:
    with pytest.raises(ValueError, match="Unknown LLM provider"):
        get_provider(Settings(llm_provider="does-not-exist"))
