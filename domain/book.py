from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Book(models.Model):

    id = fields.UUIDField(primary_key=True)
    text = fields.TextField()
    author = fields.TextField()
    tag = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)


Book_Pydantic = pydantic_model_creator(Book, name="Book")
BookDto_Pydantic = pydantic_model_creator(Book, name="BookDto", exclude_readonly=True)
