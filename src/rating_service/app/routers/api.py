from fastapi import APIRouter

from routers import rating, manage


router = APIRouter()
router.include_router(rating.router)
router.include_router(manage.router)
