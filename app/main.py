import sys
import os

# Add project root to sys.path to allow running script directly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from fastapi import FastAPI
from app.core.config import settings
from app.core.logging_config import logger

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Application is starting up...")
    yield
    logger.info("🛑 Application is shutting down...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)


from app.api.v1.api import api_router
app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    import uvicorn
    # Use the string import "app.main:app" for reload to work
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)


@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI Base System"}
