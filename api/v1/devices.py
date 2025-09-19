import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from models.devices import Device
from schemas.devices import DeviceResponse, DeviceCreate, DeviceUpdate
import crud.devices as device_crud
from db.database import get_async_session

router = APIRouter(
    prefix='/devices',
    tags=['Устройства']
)

# Создание устройства
@router.post("/", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED)
async def create_device(device_in: DeviceCreate, session: AsyncSession = Depends(get_async_session)):
    existing = await device_crud.get_device_by_inventary_number(session, device_in.inventary_number)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Device with this inventary number already exists."
        )
    new_device = await device_crud.create_device(session, device_in)
    return new_device

# Получение списка устройств
@router.get("/", response_model=List[DeviceResponse])
async def read_devices(session: AsyncSession = Depends(get_async_session)):
    devices = await device_crud.get_devices(session)
    return devices

# Получение устройства по ID
@router.get("/{device_id}", response_model=DeviceResponse)
async def read_device(device_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
    device = await device_crud.get_device(session, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device

# Обновление устройства полностью
@router.put("/{device_id}", response_model=DeviceResponse)
async def update_device(device_id: uuid.UUID, device_in: DeviceUpdate, session: AsyncSession = Depends(get_async_session)):
    device = await device_crud.get_device(session, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    updated_device = await device_crud.update_device(session, device_id, device_in)
    return updated_device

# Частичное обновление устройства
@router.patch("/{device_id}", response_model=DeviceResponse)
async def partial_update_device(device_id: uuid.UUID, device_in: DeviceUpdate, session: AsyncSession = Depends(get_async_session)):
    device = await device_crud.get_device(session, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    updated_device = await device_crud.update_device(session, device_id, device_in)
    return updated_device

# Удаление устройства
@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_device(device_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
    device = await device_crud.get_device(session, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    await device_crud.delete_device(session, device_id)



