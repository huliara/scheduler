from fastapi import APIRouter

router = APIRouter()

from .delete import router as delete
from .get import router as get
from .get_all import router as get_all
from .patch import router as patch
from .post import router as post

router.include_router(delete)
router.include_router(get_all)
router.include_router(patch)
router.include_router(post)
router.include_router(get)