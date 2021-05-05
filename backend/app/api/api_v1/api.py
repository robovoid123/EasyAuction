from fastapi import APIRouter
from .endpoints import users, products

router = APIRouter()

router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(products.router, prefix="/products", tags=["products"])
