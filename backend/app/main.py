from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.utils.schedule import sched
from app.db.init_db import init_db
from app.api import router


def append_routes(app):
    app.include_router(router, prefix=settings.API_PREFIX)


def create_app():
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_PREFIX}/v1/openapi.json",
        version=1.0
    )

    # Set all CORS enabled origins
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in
                           settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # initialize database
    init_db()

    # start APScheduler
    sched.start()

    append_routes(app)

    return app


app = create_app()
