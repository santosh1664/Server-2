from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    api_key: str = "development-only-change-me"

    captcha_demo_enabled: bool = False
    demo_challenge_ttl_seconds: int = 60
    demo_max_attempts: int = 3

    browser_headless: bool = True
    browser_timeout_seconds: int = 25

    rejekt_callback_url: str | None = None
    rejekt_callback_secret: str | None = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
