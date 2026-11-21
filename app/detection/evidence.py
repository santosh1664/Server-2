from dataclasses import dataclass, field


@dataclass
class PageEvidence:
    page_url: str
    title: str = ""
    provider_hints: list[str] = field(default_factory=list)
    indicators: list[str] = field(default_factory=list)
    collected_at: str | None = None
