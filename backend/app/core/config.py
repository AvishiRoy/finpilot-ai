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

    # No default value here on purpose: if DATABASE_URL is missing from
    # the environment, Settings() will raise a validation error at startup
    # rather than letting the app run with no database connection at all.
    database_url: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()