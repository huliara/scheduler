from fastapi import APIRouter

router = APIRouter()

from .activate_user import router as activate_user
from .add_group_member import router as add_group_member
from .adminate_user import router as adminate_user
from .delete_group import router as delete_group
from .delete_user import router as delete_user
from .get_group import router as get_group
from .get_user import router as get_user
from .get_users import router as get_users
from .patch_group import router as patch_group
from .patch_user import router as patch_user
from .post_group import router as post_groups
from .post_user import router as post_user

router.include_router(activate_user)
router.include_router(add_group_member)
router.include_router(adminate_user)
router.include_router(delete_group)
router.include_router(delete_user)
router.include_router(get_group)
router.include_router(get_user)
router.include_router(get_users)
router.include_router(patch_group)
router.include_router(patch_user)
router.include_router(post_groups)
router.include_router(post_user)