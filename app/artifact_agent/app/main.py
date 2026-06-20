from fastapi import FastAPI
import uvicorn

from app.src.api.routes.router import router


app = FastAPI(
    title="General Purpose Agent API",
    version="1.0.0"
)


app.include_router(router)


