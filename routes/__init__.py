from fastapi import APIRouter, Depends

from .spider import router as spider_router
from .user import router as user_router
from .task import router as task_router
from .book import router as book_router

router = APIRouter()
router.include_router(spider_router)
router.include_router(user_router)
router.include_router(task_router)
router.include_router(book_router)
