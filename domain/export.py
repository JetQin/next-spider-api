from enum import Enum

from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class RequestStatus(str, Enum):
    UNKNOW="UNKNOW"
    APPROVED="APPROVED"
    DECLINED="DECLINED"


class ExportRequest(models.Model):
    """
    The export request model
    """

    id = fields.UUIDField(primary_key=True)
    #: This is a username
    table = fields.TextField()
    reason = fields.TextField()
    requester = fields.CharField(max_length=50, null=True)
    approver = fields.CharField(max_length=50, null=True)
    status = fields.CharEnumField(RequestStatus, "Export request status")
    comment = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)


ExportDao = pydantic_model_creator(ExportRequest, name="ExportRequestDao")
ExportDto = pydantic_model_creator(ExportRequest, name="ExportRequestDto", exclude_readonly=True)
