from fastapi import APIRouter

# from app.modules.auction.api import router as auction_router
from app.modules.product.api import router as product_router
from app.modules.user.api import router as user_router

router = APIRouter()
# router.include_router(auction_router)
router.include_router(product_router)
router.include_router(user_router)
