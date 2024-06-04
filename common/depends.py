from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.params import Path
from starlette.requests import Request
from starlette.status import HTTP_404_NOT_FOUND
from tortoise import Tortoise


def get_model(resource: Optional[str] = Path(...)):
    if not resource:
        return
    for app, models in Tortoise.apps.items():
        models = {key.lower(): val for key, val in models.items()}
        model = models.get(resource)
        if model:
            return model

