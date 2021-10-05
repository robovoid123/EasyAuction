from typing import Optional

from pydantic import BaseModel


class NotificationBase(BaseModel):
    title: Optional[str]
    detail: Optional[str] = ''
    sender_id: Optional[int]
    reciever_id: Optional[int]


class NotificationCreate(NotificationBase):
    title: str
    sender_id: int
    reciever_id: int


class NotificationUpdate(NotificationBase):
    pass


class NotificationInDB(NotificationBase):
    id: Optional[int] = None
    active: Optional[bool]

    class Config:
        orm_mode = True


class Notification(NotificationInDB):
    pass
