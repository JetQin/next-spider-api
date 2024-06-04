from typing import List
from fastapi import APIRouter
from domain.book import Book, Book_Pydantic
from pydantic import BaseModel

router = APIRouter(prefix="/book", tags=["book"])


class Status(BaseModel):
    message: str


@router.get("/book", response_model=List[Book_Pydantic])
async def get_books():
    return await Book_Pydantic.from_queryset(Book.all())

