from fastapi import APIRouter

router=APIRouter()
from .get_all import router as get_all

router.include_router(get_all)
