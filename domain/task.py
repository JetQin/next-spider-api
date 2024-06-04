import enum

from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Spider(enum.IntEnum):
    BOOK = 0


class TaskStatus(enum.IntEnum):
    INIT = 0
    DONE = 1


class Task(models.Model):
    """
    The User model
    """

    id = fields.UUIDField(primary_key=True)
    name = fields.TextField()
    domain = fields.TextField()
    spider = fields.TextField()
    status = fields.IntEnumField(TaskStatus, "task status")
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    def get_status(self) -> str:
        """
        Returns the best name
        """
        if self.name and self.status:
            return f"{self.name or ''} {self.status.value or ''}".strip()
        return self.name


Task_Pydantic = pydantic_model_creator(Task, name="Task")
TaskDto_Pydantic = pydantic_model_creator(Task, name="TaskDto", exclude_readonly=True)
