from fastapi import FastAPI

from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import text

from src.utils.db import Base, engine
from src.user.routers import router as users_router, transfer_router
from src.utils.auth import create_access_token
from fastapi import Depends
from src.utils.permissions import require_admin


def create_app() -> FastAPI:
    app = FastAPI(title="Fake Bank")

    # include routers
    app.include_router(users_router)
    app.include_router(transfer_router)

    @app.on_event("startup")
    async def on_startup() -> None:
        # асинхронное создание таблиц
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @app.post("/auth/token")
    async def issue_token(username: str, _=Depends(require_admin)):
        # простая выдача токена по админ-заголовку для тестирования
        return {"access_token": create_access_token(username)}

    return app


app = create_app()


