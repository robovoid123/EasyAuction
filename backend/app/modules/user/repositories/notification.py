from app.repository.repository_base import BaseRepository
from typing import Any, Dict, Optional, Union

from sqlalchemy.orm.session import Session

from app.modules.user.models import Notification
from app.modules.user.schemas import NotificationCreate, NotificationUpdate


class NotificationRepository(BaseRepository[Notification, NotificationCreate, NotificationUpdate]):

    def get_user_notification(
        self, db: Session, *, skip: int = 0, limit: int = 100, user_id: int, active=True
    ):
        return db.query(self.model).filter(self.model.reciever_id == user_id).filter(self.model.active == active).offset(skip).limit(limit).all()

    def read_notification(
        self, db: Session, db_obj: Notification
    ):
        return self.update(db, db_obj=db_obj, obj_in={'active': False})


notification_repo = NotificationRepository(Notification)
