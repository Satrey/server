from fastapi import APIRouter, FastAPI
from contextlib import asynccontextmanager

from api.v1 import users, devices, rtobjects
from api.v1 import device_types, device_models, device_manufacturers


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
main_router.include_router(devices.router)
main_router.include_router(rtobjects.router)
main_router.include_router(device_types.router)
main_router.include_router(device_models.router)
main_router.include_router(device_manufacturers.router)

app.include_router(main_router, prefix="/api/v1")


