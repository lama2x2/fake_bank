from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_host: str = "db"
    database_port: int = 5432
    database_user: str = "postgres"
    database_password: str = "postgres"
    database_name: str = "fake_bank"

    # простейший токен для админ-доступа в примере
    admin_token: str = "secret"

    class Config:
        env_prefix = "APP_"
        env_file = ".env"


settings = Settings()


