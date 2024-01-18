from fastapi import APIRouter

from routers import library, book, library_book, manage


router = APIRouter()
router.include_router(library.router)
router.include_router(book.router)
router.include_router(library_book.router)
router.include_router(manage.router)
