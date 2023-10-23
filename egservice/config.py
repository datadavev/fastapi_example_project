import os
import pydantic_settings


BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))


class Settings(pydantic_settings.BaseSettings):
    # env_prefix provides the environment variable prefix
    # for overriding these settings with env vars.
    # e.g. EGSERVICE_PORT=11000
    model_config = pydantic_settings.SettingsConfigDict(env_prefix="EGSERVICE_")
    host: str = "localhost"
    port: int = 8000
    protocol: str = "http"
    static_dir: str = os.path.join(BASE_FOLDER, "static")
    template_dir: str = os.path.join(BASE_FOLDER, "templates")


settings = Settings()
