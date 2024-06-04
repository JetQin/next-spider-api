import uuid
from typing import List
from fastapi import APIRouter
from domain.export import ExportRequest, ExportDao, ExportDto
from pydantic import BaseModel

router = APIRouter(tags=["export"])


class Status(BaseModel):
    message: str


@router.get("/list", response_model=List[ExportDao])
async def list_export():
    return await ExportDao.from_queryset(ExportRequest.all())


@router.post("/create", response_model=ExportDao)
async def create_export_request(req: ExportDto):
    request = await ExportRequest.create(**req.model_dump(exclude_unset=True))
    return await ExportDao.from_tortoise_orm(request)


@router.put("/update/{request_id}", response_model=ExportDao)
async def update_export_request(request_id: str, req: ExportDto):
    await ExportRequest.filter(id=request_id).update(**req.model_dump(exclude_unset=True))
    return await ExportDao.from_queryset_single(ExportRequest.get(id=request_id))



