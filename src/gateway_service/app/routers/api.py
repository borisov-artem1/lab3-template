from fastapi import APIRouter

from routers import gateway

router = APIRouter()
router.include_router(gateway.router)
