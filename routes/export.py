import sqlite3
import io
import pandas as pd
from typing import List
from fastapi import APIRouter
from starlette.responses import StreamingResponse, JSONResponse

from domain.export import  RequestStatus, ExportRequest, ExportDao, ExportDto
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


@router.get("/export_csv/{request_id}")
async def export_csv(request_id: str):
    request = await ExportDao.from_queryset_single(ExportRequest.get(id=request_id))
    table = request.table
    status = request.status
    if status != RequestStatus.APPROVED:
        return JSONResponse({"msg": "Request not approved!"})
    with sqlite3.connect('data/spider.db') as connection:
        df = pd.read_sql_query("select * from {}".format(table), connection)
        stream = io.StringIO()
        df.to_csv(stream, index=False)
        response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
        response.headers["Content-Disposition"] = "attachment; filename=export.csv"
        return response
