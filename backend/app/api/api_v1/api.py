from fastapi import APIRouter
from .endpoints import users, login, products, auction

router = APIRouter()

router.include_router(login.router, prefix="/auth", tags=["Auth"])
router.include_router(users.router, prefix="/users", tags=["Users"])
router.include_router(products.router, prefix="/products", tags=["Products"])
router.include_router(auction.router, prefix="/auctions", tags=["Auctions"])
