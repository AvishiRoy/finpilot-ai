from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Centralized application configuration.

    All environment-dependent values are declared here with explicit types.
    Pydantic validates these at startup — if a required variable is missing
    or has the wrong type, the application fails fast with a clear error
    instead of failing unpredictably later.
    """

    app_name: str = "FinPilot AI"
    app_env: str = "development"
    debug: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


# A single, shared instance imported everywhere config is needed.
# This avoids re-reading and re-validating the .env file in multiple places.
settings = Settings()