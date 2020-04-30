from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from .dependencies import injector
from .views import router
from ..config import Config


def setup_application(config: Config) -> FastAPI:
    application = FastAPI(
        docs_url="/docs" if config.ENABLE_API_DOCS else None,
        redoc_url="/redoc" if config.ENABLE_API_DOCS else None,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.mount(
        "/static",
        StaticFiles(directory=str(Path(__file__).parent.resolve() / "static")),
        name="static",
    )
    application.include_router(router)
    return application


app = setup_application(injector.get(Config))
