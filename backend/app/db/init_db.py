from sqlalchemy.orm import Session

from app.modules.user.schemas import UserCreate
from app.modules.user.repositories import user_repo
from app.core.config import settings
from app.db import base  # noqa: F401
from app.db.session import engine, SessionLocal


def init_db() -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    print("Creating Database")
    base.Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        user = user_repo.get_by_email(db, email=settings.FIRST_SUPERUSER)
        if not user:
            user_in = UserCreate(
                email=settings.FIRST_SUPERUSER,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                is_superuser=True,
            )
            user = user_repo.create(db, obj_in=user_in)  # noqa: F841
