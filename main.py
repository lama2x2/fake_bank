from fastapi import FastAPI

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
    def on_startup() -> None:
        Base.metadata.create_all(bind=engine)

    @app.post("/auth/token")
    def issue_token(username: str, _=Depends(require_admin)):
        # простая выдача токена по админ-заголовку для тестирования
        return {"access_token": create_access_token(username)}

    return app


app = create_app()


