from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.dependencies import database, auth

from app.modules.user.repositories import notification_repo
from app.modules.user.schemas import NotificationCreate, NotificationUpdate, NotificationInDB
from app.modules.user.models import User

router = APIRouter()


@router.post("/create", response_model=NotificationInDB)
def create_a_notification(
    notification_data: NotificationCreate,
    db: Session = Depends(database.get_db)
):
    return notification_repo.create(db, obj_in=notification_data)


@router.get("/me", response_model=List[NotificationInDB])
def get_my_notification(
    db: Session = Depends(database.get_db),
    current_user: User = Depends(auth.get_current_active_user)
):
    return notification_repo.get_user_notification(db, skip=0, limit=100, user_id=current_user.id)


@router.post("/read/{id}")
def read_notification(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(auth.get_current_active_user)
):
    db_obj = notification_repo.get(db, id=id)
    if db_obj:
        return notification_repo.read_notification(db=db, db_obj=db_obj)
