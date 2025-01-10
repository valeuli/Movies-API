from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.database_settings import engine, Base
from app.routers.user import user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(user_router, prefix="/user", tags=["user"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
