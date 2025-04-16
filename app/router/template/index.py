from fastapi import APIRouter

router = APIRouter()

from .add_slot import router as add_slot
from .delete import router as delete
from .delete_slot import router as delete_slot
from .generate_task import router as generate_task
from .get import router as get
from .get_all import router as get_all
from .patch_name import router as patch_name
from .patch_slot import router as patch_slots
from .post import router as post

router.include_router(delete)
router.include_router(generate_task)
router.include_router(patch_slots)
router.include_router(patch_name)
router.include_router(post)
router.include_router(get)
router.include_router(get_all)
router.include_router(delete_slot)
router.include_router(add_slot)

    