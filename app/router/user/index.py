from fastapi import APIRouter, Depends

router = APIRouter()

from .get import router as get_user_profile
from .get_relate_taskdetail import router as get_relate_taskdetail
from .getall_tasks import router as get_all_tasks
from .update_password import router as update_password
from .update_profile import router as update_profile

router.include_router(get_user_profile)
router.include_router(get_all_tasks)
router.include_router(update_password)
router.include_router(update_profile)
router.include_router(get_relate_taskdetail)