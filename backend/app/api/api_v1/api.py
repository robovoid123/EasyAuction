from fastapi import APIRouter
from .endpoints import users, login

router = APIRouter()

router.include_router(login.router, prefix="/auth", tags=["Auth"])
router.include_router(users.router, tags=["users"])
