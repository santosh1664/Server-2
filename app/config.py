from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    api_key: str = "development-only-change-me"

    captcha_demo_enabled: bool = False
    demo_challenge_ttl_seconds: int = 60
    demo_max_attempts: int = 3

    browser_headless: bool = True
    browser_timeout_seconds: int = 25

    # Provider secrets must be stored in the deployment environment, never Git.
    recaptcha_secret_key: str | None = None
    recaptcha_allowed_hostnames: str = ""
    recaptcha_expected_action: str | None = None
    recaptcha_minimum_score: float = 0.5

    hcaptcha_secret_key: str | None = None
    hcaptcha_sitekey: str | None = None
    hcaptcha_allowed_hostnames: str = ""

    turnstile_secret_key: str | None = None
    turnstile_allowed_hostnames: str = ""
    turnstile_expected_action: str | None = None

    provider_verify_timeout_seconds: float = 8.0

    rejekt_callback_url: str | None = None
    rejekt_callback_secret: str | None = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
