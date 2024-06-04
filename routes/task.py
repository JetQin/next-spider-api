import os
from typing import List
from fastapi import APIRouter
from fastapi import HTTPException
from domain.task import Task, TaskDao, TaskDto
from pydantic import BaseModel

router = APIRouter(tags=["task"])


class Status(BaseModel):
    message: str


@router.get("/task", response_model=List[TaskDao])
async def get_tasks():
    return await TaskDao.from_queryset(Task.all())


@router.post("/task", response_model=TaskDao)
async def create_task(task: TaskDto):
    task_obj = await Task.create(**task.model_dump(exclude_unset=True))
    return await TaskDao.from_tortoise_orm(task_obj)


@router.get("/task/{task_id}", response_model=TaskDao)
async def get_task(task_id: int):
    return await TaskDao.from_queryset_single(Task.get(id=task_id))


@router.put("/task/{task_id}", response_model=TaskDao)
async def update_task(task_id: int, task: TaskDao):
    await Task.filter(id=task_id).update(**task.model_dump(exclude_unset=True))
    return await TaskDao.from_queryset_single(Task.get(id=task_id))


@router.delete("/task/{task_id}", response_model=Status)
async def delete_task(task_id: int):
    deleted_count = await Task.filter(id=task_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"task {task_id} not found")
    return Status(message=f"Deleted task {task_id}")