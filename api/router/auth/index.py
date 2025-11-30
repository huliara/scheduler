from fastapi import APIRouter

router = APIRouter()
from .login import router as login
from .signup import router as signup

router.include_router(login)
router.include_router(signup)