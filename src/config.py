from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_host: str = "db"
    database_port: int = 5432
    database_user: str = "postgres"
    database_password: str = "postgres"
    database_name: str = "fake_bank"

    class Config:
        env_prefix = "APP_"
        env_file = ".env"


settings = Settings()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


class Base(DeclarativeBase):
    pass


def _build_connection_url() -> str:
    return (
        f"postgresql+psycopg2://{settings.database_user}:{settings.database_password}"
        f"@{settings.database_host}:{settings.database_port}/{settings.database_name}"
    )


engine = create_engine(_build_connection_url(), pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


