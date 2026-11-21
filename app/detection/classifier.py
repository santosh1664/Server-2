from dataclasses import dataclass

@dataclass
class Detection:
    providers: list[str]
    evidence: list[str]
    @property
    def detected(self) -> bool:
        return bool(self.evidence)

SIGNATURES = {
    "recaptcha": ("google.com/recaptcha", "gstatic.com/recaptcha", "g-recaptcha"),
    "hcaptcha": ("hcaptcha.com", "h-captcha"),
    "turnstile": ("challenges.cloudflare.com/turnstile", "cf-turnstile"),
    "cloudflare": ("cf-chl-", "challenge-platform"),
}

def classify_evidence(url: str, html: str, visible_text: str) -> Detection:
    haystack = "\n".join((url, html, visible_text)).lower()
    providers, evidence = [], []
    for provider, signatures in SIGNATURES.items():
        matches = [sig for sig in signatures if sig in haystack]
        if matches:
            providers.append(provider)
            evidence.extend(f"{provider}: matched '{match}'" for match in matches)
    for phrase in ("verify you are human", "unusual traffic",
                   "complete the security check", "security verification required"):
        if phrase in haystack:
            evidence.append(f"generic: visible phrase '{phrase}'")
    return Detection(sorted(set(providers)), evidence)
