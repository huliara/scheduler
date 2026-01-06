from fastapi import APIRouter

router = APIRouter()
from .assign import router as assign
from .bulk_delete import router as bulk_delete
from .cancel import router as cancel
from .complete import router as complete
from .delete import router as delete
from .get import router as get
from .get_all import router as get_all
from .patch import router as patch
from .post import router as post
from .delete_orphan import router as delete_orphan

router.include_router(assign)
router.include_router(bulk_delete)
router.include_router(delete_orphan)
router.include_router(cancel)
router.include_router(complete)
router.include_router(delete)
router.include_router(get)
router.include_router(get_all)
router.include_router(patch)
router.include_router(post)