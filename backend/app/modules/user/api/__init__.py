from fastapi import APIRouter
from .v1 import users, login, notification

router = APIRouter()

router.include_router(users.router, prefix="/users", tags=["User"])
router.include_router(login.router, prefix="/auth", tags=["Auth"])
router.include_router(notification.router, prefix="/notification", tags=["Notification"])
