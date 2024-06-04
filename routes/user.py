import os
from typing import List
from fastapi import APIRouter
from fastapi import HTTPException
from domain.users import Users, UserDao, UserDto
from pydantic import BaseModel

router = APIRouter(tags=["user"])


class Status(BaseModel):
    message: str


@router.get("/users", response_model=List[UserDao])
async def get_users():
    return await UserDao.from_queryset(Users.all())


@router.post("/users", response_model=UserDao)
async def create_user(user: UserDto):
    user_obj = await Users.create(**user.model_dump(exclude_unset=True))
    return await UserDao.from_tortoise_orm(user_obj)


@router.get("/user/{user_id}", response_model=UserDao)
async def get_user(user_id: int):
    return await UserDao.from_queryset_single(Users.get(id=user_id))


@router.put("/user/{user_id}", response_model=UserDao)
async def update_user(user_id: int, user: UserDto):
    await Users.filter(id=user_id).update(**user.model_dump(exclude_unset=True))
    return await UserDao.from_queryset_single(Users.get(id=user_id))


@router.delete("/user/{user_id}", response_model=Status)
async def delete_user(user_id: int):
    deleted_count = await Users.filter(id=user_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return Status(message=f"Deleted user {user_id}")