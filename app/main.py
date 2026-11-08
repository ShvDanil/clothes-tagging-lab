from collections.abc import Iterator
from contextlib import asynccontextmanager
from typing import Annotated, Any

from fastapi import Depends, FastAPI, File, HTTPException, Request, UploadFile
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app import service
from app.config import Settings
from app.db import Database


def get_session(request: Request) -> Iterator[Session]:
    with request.app.state.database.session_factory() as session:
        yield session


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings()
    database = Database(settings.database_url)

    @asynccontextmanager
    async def lifespan(application: FastAPI):
        try:
            database.initialize()
            yield
        finally:
            database.close()

    application = FastAPI(title="Clothes tagging lab", version="0.1.0", lifespan=lifespan)
    application.state.database = database
    application.state.settings = settings

    @application.get("/health", tags=["infrastructure"])
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @application.get("/ready", tags=["infrastructure"])
    def ready() -> dict[str, str]:
        try:
            database.check()
        except SQLAlchemyError:
            raise HTTPException(status_code=503, detail="Database unavailable") from None
        return {"status": "ready"}

    @application.post("/annotate", tags=["annotation"])
    def annotate(
        images: Annotated[
            list[UploadFile],
            File(description="Photos of one clothing item and colour variant; repeat this field"),
        ],
        session: Annotated[Session, Depends(get_session)],
    ) -> dict[str, Any]:
        if not 1 <= len(images) <= settings.max_images_per_item:
            raise HTTPException(
                status_code=422,
                detail=f"Provide 1 to {settings.max_images_per_item} images of one item",
            )
        try:
            return service.annotate_images(images=images, session=session)
        except service.AnnotationNotImplementedError:
            raise HTTPException(
                status_code=501,
                detail="Annotation pipeline is not implemented in the starter",
            ) from None

    return application


app = create_app()
