from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_host: str
    database_port: int
    database_user: str
    database_password: str
    database_name: str

    # простейший токен для админ-доступа в примере
    admin_token: str
    jwt_secret: str
    jwt_algorithm: str

    # pydantic-settings v2 style config
    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_file=".env",
        extra="ignore",  # игнорировать посторонние ключи в .env (например POSTGRES_*)
    )


settings = Settings()


