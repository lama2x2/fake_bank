from fastapi import FastAPI

from src.config import Base, engine
from src.user.routers import router as users_router, transfer_router


def create_app() -> FastAPI:
    app = FastAPI(title="Fake Bank")

    # include routers
    app.include_router(users_router)
    app.include_router(transfer_router)

    @app.on_event("startup")
    def on_startup() -> None:
        Base.metadata.create_all(bind=engine)

    return app


app = create_app()


