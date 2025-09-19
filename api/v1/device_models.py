import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from db.database import get_async_session
from schemas.devices import DeviceModelResponse, DeviceModelCreate, DeviceModelUpdate

import crud.device_models as device_model_crud

router = APIRouter(
    prefix='/device-models',
    tags=['Модели устройств']
)

@router.post("/", response_model=DeviceModelResponse, status_code=status.HTTP_201_CREATED)
async def create_device_model(model_in: DeviceModelCreate, session: AsyncSession = Depends(get_async_session)):
    existing = await device_model_crud.get_device_model_by_name(session, model_in.name)
    if existing:
        raise HTTPException(status_code=400, detail="Device model with this name already exists")
    model = await device_model_crud.create_device_model(session, model_in)
    return model

@router.get("/", response_model=List[DeviceModelResponse])
async def read_device_models(skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_async_session)):
    models = await device_model_crud.get_device_models(session, skip=skip, limit=limit)
    return models

@router.get("/{model_id}", response_model=DeviceModelResponse)
async def read_device_model(model_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
    model = await device_model_crud.get_device_model(session, model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Device model not found")
    return model

@router.patch("/{model_id}", response_model=DeviceModelResponse)
async def update_device_model(model_id: uuid.UUID, model_in: DeviceModelUpdate, session: AsyncSession = Depends(get_async_session)):
    model = await device_model_crud.get_device_model(session, model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Device model not found")
    model = await device_model_crud.update_device_model(session, model, model_in)
    return model

@router.delete("/{model_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_device_model(model_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
    model = await device_model_crud.get_device_model(session, model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Device model not found")
    await device_model_crud.delete_device_model(session, model)
    return None