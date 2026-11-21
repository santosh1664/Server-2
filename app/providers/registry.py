from app.providers.base import VerificationAdapter

class ProviderRegistry:
    def __init__(self):
        self._adapters: dict[str, VerificationAdapter] = {}
    def register(self, adapter: VerificationAdapter) -> None:
        if adapter.provider in self._adapters:
            raise ValueError(f"Provider already registered: {adapter.provider}")
        self._adapters[adapter.provider] = adapter
    def get(self, provider: str) -> VerificationAdapter | None:
        return self._adapters.get(provider)
    def names(self) -> list[str]:
        return sorted(self._adapters)

registry = ProviderRegistry()
