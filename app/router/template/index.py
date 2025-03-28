from fastapi import APIRouter

router = APIRouter()

from .delete import router as delete
from .generate_task import router as generate_task
from .get import router as get
from .get_all import router as get_all
from .patch_name import router as patch_name
from .patch_slots import router as patch_slots
from .post import router as post

router.include_router(delete)
router.include_router(generate_task)
router.include_router(patch_slots)
router.include_router(patch_name)
router.include_router(post)
router.include_router(get)
router.include_router(get_all)
    