from fastapi import APIRouter

from routers import reservation, manage


router = APIRouter()
router.include_router(reservation.router)
router.include_router(manage.router)
