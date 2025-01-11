from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, status, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.database_settings import engine, Base
from app.routers.movie import movie_router
from app.routers.user import user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    details = exc.errors()
    modified_details = []
    for error in details:
        message = f"Error in field '{error['loc'][1]}': {error['msg']}"
        modified_details.append(
            {
                "error": {
                    "code": error["type"].upper(),
                    "message": message,
                }
            }
        )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": modified_details}),
    )


app.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(movie_router, prefix="/movie", tags=["movie"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
