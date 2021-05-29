from fastapi import APIRouter
from .api_v1 import router as v1_rotuer

router = APIRouter()
router.include_router(v1_rotuer, prefix="/v1")
