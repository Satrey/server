import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from db.database import get_async_session
from models.devices import Device, DeviceType
from schemas.devices import DeviceTypeRead, DeviceTypeCreate, DeviceTypeUpdate

import crud.device as device_crud


router = APIRouter(
    prefix='/devices',
    tags=['Devices']
)

@router.post("/types", response_model=DeviceTypeRead, status_code=status.HTTP_201_CREATED)
async def create_user(device_type_in: DeviceTypeCreate, session: AsyncSession = Depends(get_async_session)):
    existing = await device_crud.get_device_type_by_name(session, device_type_in.name)
    if existing:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    device_type = await device_crud.create_device_type(session, device_type_in)
    return device_type

@router.get("/types", response_model=List[DeviceTypeRead])
async def read_device_types(skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_async_session)):
    device_types = await device_crud.get_device_types(session, skip=skip, limit=limit)
    return device_types

@router.get("/types/by/{name}", response_model=DeviceTypeRead)
async def read_device_type_by_name(device_type_name: str, session: AsyncSession = Depends(get_async_session)):
    device_type = await device_crud.get_device_type_by_name(session, device_type_name)
    return device_type

@router.get("/types/{device_type_id}", response_model=DeviceTypeRead)
async def read_device_type_by_id(device_type_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
    device_type = await device_crud.get_device_type(session, device_type_id)
    return device_type

@router.patch("/types/{device_type_id}", response_model=DeviceTypeRead)
async def update_user(device_type_id: uuid.UUID, device_type_in: DeviceTypeUpdate, session: AsyncSession = Depends(get_async_session)):
    device_type = await device_crud.get_device_type(session, device_type_id)
    if not device_type:
        raise HTTPException(status_code=404, detail="Device type not found")
    device_type = await device_crud.update_device_type(session, device_type, device_type_in)
    return device_type

@router.delete("/types/{device_type_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(device_type_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
    device_type = await device_crud.get_device_type(session, device_type_id)
    if not device_type:
        raise HTTPException(status_code=404, detail="Device type not found")
    await device_crud.delete_device_type(session, device_type)
    return None


