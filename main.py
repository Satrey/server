from fastapi import APIRouter, FastAPI
from contextlib import asynccontextmanager

from api.v1 import users


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    print("Server start")
    yield
    # Clean up the ML models and release the resources
    print("Server stop")

app = FastAPI(lifespan=lifespan)

main_router = APIRouter()
main_router.include_router(users.router)

app.include_router(main_router, prefix="/api/v1")


