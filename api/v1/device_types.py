import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from db.database import get_async_session
from schemas.devices import DeviceTypeResponse, DeviceTypeCreate, DeviceTypeUpdate

import crud.device_types as device_type_crud

router = APIRouter(
    prefix='/device-types',
    tags=['Типы устройств']
)

@router.post("/", response_model=DeviceTypeResponse, status_code=status.HTTP_201_CREATED)
async def create_device_type(type_in: DeviceTypeCreate, session: AsyncSession = Depends(get_async_session)):
    existing = await device_type_crud.get_device_type_by_name(session, type_in.name)
    if existing:
        raise HTTPException(status_code=400, detail="Device type with this name already exists")
    device_type = await device_type_crud.create_device_type(session, type_in)
    return device_type

@router.get("/", response_model=List[DeviceTypeResponse])
async def read_device_types(skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_async_session)):
    types = await device_type_crud.get_device_types(session, skip=skip, limit=limit)
    return types

@router.get("/{type_id}", response_model=DeviceTypeResponse)
async def read_device_type(type_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
    device_type = await device_type_crud.get_device_type(session, type_id)
    if not device_type:
        raise HTTPException(status_code=404, detail="Device type not found")
    return device_type

@router.patch("/{type_id}", response_model=DeviceTypeResponse)
async def update_device_type(type_id: uuid.UUID, type_in: DeviceTypeUpdate, session: AsyncSession = Depends(get_async_session)):
    device_type = await device_type_crud.get_device_type(session, type_id)
    if not device_type:
        raise HTTPException(status_code=404, detail="Device type not found")
    device_type = await device_type_crud.update_device_type(session, device_type, type_in)
    return device_type

@router.delete("/{type_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_device_type(type_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
    device_type = await device_type_crud.get_device_type(session, type_id)
    if not device_type:
        raise HTTPException(status_code=404, detail="Device type not found")
    await device_type_crud.delete_device_type(session, device_type)
    return None