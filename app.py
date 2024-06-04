from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI
from tortoise.contrib.fastapi import RegisterTortoise
from routes import router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # app startup
    async with RegisterTortoise(
        app,
        db_url="sqlite://data/spider.db",
        modules={"domain": ["domain.users", "domain.task", "domain.book"]},
        generate_schemas=True,
        add_exception_handlers=True,
    ):
        # await connectToDatabase()
        yield
        # app teardown
    # db connections closed

app = FastAPI(
    title="Next Spider API",
    description="Next Spider Api service",
    lifespan=lifespan
)
app.include_router(router)


if __name__ == '__main__':
    uvicorn.run(app=app)
