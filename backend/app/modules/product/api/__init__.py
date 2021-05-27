from fastapi import APIRouter
from .v1 import products, categories

router = APIRouter()

router.include_router(products.router, prefix="/products", tags=["Products"])
router.include_router(categories.router, prefix="/categories", tags=["Categories"])
