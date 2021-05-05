from fastapi import APIRouter
from .endpoints import users, login, products

router = APIRouter()

router.include_router(login.router, prefix="/auth", tags=["Auth"])
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(products.router, prefix="/products", tags=["products"])
