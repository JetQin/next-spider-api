from typing import List
from fastapi import APIRouter
from domain.book import Book, BookDao
from pydantic import BaseModel

router = APIRouter(tags=["book"])


class Status(BaseModel):
    message: str


@router.get("/book", response_model=List[BookDao])
async def get_books():
    return await BookDao.from_queryset(Book.all())

