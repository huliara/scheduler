from fastapi import APIRouter, Depends

router = APIRouter()

from .update_password import router as update_password
from .update_profile import router as update_profile


router.include_router(update_password)
router.include_router(update_profile)