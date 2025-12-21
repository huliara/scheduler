from fastapi import APIRouter

router=APIRouter()
from .get import router as get
from .get_all import router as get_all
from .member.index import router as member
from .post import router as post

router.include_router(member, prefix="/{group_id}/members")
router.include_router(get_all)
router.include_router(get)
router.include_router(post)
