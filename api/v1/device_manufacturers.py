import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from db.database import get_async_session
from schemas.devices import DeviceManufacturerResponse, DeviceManufacturerCreate, DeviceManufacturerUpdate

import crud.device_manufacturers as device_manufacturer_crud

router = APIRouter(
    prefix='/device-manufacturers',
    tags=['Производители устройств']
)

@router.post("/", response_model=DeviceManufacturerResponse, status_code=status.HTTP_201_CREATED)
async def create_device_manufacturer(manufacturer_in: DeviceManufacturerCreate, session: AsyncSession = Depends(get_async_session)):
    existing = await device_manufacturer_crud.get_device_manufacturer_by_name(session, manufacturer_in.name)
    if existing:
        raise HTTPException(status_code=400, detail="Manufacturer with this name already exists")
    manufacturer = await device_manufacturer_crud.create_device_manufacturer(session, manufacturer_in)
    return manufacturer

@router.get("/", response_model=List[DeviceManufacturerResponse])
async def read_device_manufacturers(skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_async_session)):
    manufacturers = await device_manufacturer_crud.get_device_manufacturers(session, skip=skip, limit=limit)
    return manufacturers

@router.get("/{manufacturer_id}", response_model=DeviceManufacturerResponse)
async def read_device_manufacturer(manufacturer_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
    manufacturer = await device_manufacturer_crud.get_device_manufacturer(session, manufacturer_id)
    if not manufacturer:
        raise HTTPException(status_code=404, detail="Manufacturer not found")
    return manufacturer

@router.patch("/{manufacturer_id}", response_model=DeviceManufacturerResponse)
async def update_device_manufacturer(manufacturer_id: uuid.UUID, manufacturer_in: DeviceManufacturerUpdate, session: AsyncSession = Depends(get_async_session)):
    manufacturer = await device_manufacturer_crud.get_device_manufacturer(session, manufacturer_id)
    if not manufacturer:
        raise HTTPException(status_code=404, detail="Manufacturer not found")
    manufacturer = await device_manufacturer_crud.update_device_manufacturer(session, manufacturer, manufacturer_in)
    return manufacturer

@router.delete("/{manufacturer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_device_manufacturer(manufacturer_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
    manufacturer = await device_manufacturer_crud.get_device_manufacturer(session, manufacturer_id)
    if not manufacturer:
        raise HTTPException(status_code=404, detail="Manufacturer not found")
    await device_manufacturer_crud.delete_device_manufacturer(session, manufacturer)
    return None

