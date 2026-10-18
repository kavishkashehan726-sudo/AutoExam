from collections.abc import Callable

from app.core.config import Settings
from app.llm.base import LLMProvider

ProviderFactory = Callable[[Settings], LLMProvider]

_factories: dict[str, ProviderFactory] = {}


def register_provider(name: str, factory: ProviderFactory) -> None:
    _factories[name] = factory


def get_provider(settings: Settings) -> LLMProvider:
    try:
        factory = _factories[settings.llm_provider]
    except KeyError:
        known = ", ".join(sorted(_factories)) or "none"
        raise ValueError(
            f"Unknown LLM provider {settings.llm_provider!r} (registered: {known})"
        ) from None
    return factory(settings)
