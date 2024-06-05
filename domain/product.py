from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

class Product(models.Model):
    name = fields.TextField()
    price = fields.TextField()
    text = fields.TextField()
    id = fields.UUIDField(primary_key=True)
ProductDao = pydantic_model_creator(Product, name='ProductDao')
ProductDto = pydantic_model_creator(Product, name='ProductDto')