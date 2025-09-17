from typing import Optional
import uuid
from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from models.device import Device, DeviceType, DeviceModel, DeviceManufacturer

from schemas.device import DeviceCreate, DeviceUpdate, DeviceRead
from schemas.device import DeviceTypeCreate, DeviceTypeUpdate, DeviceTypeRead
from schemas.device import DeviceModelCreate, DeviceModelUpdate, DeviceModelRead
from schemas.device import DeviceManufacturerCreate, DeviceManufacturerUpdate, DeviceManufacturerRead


async def get_device_type(db: AsyncSession, device_type_id: uuid.UUID) -> Optional[DeviceType]:
    result = await db.execute(select(DeviceType).filter(DeviceType.id == device_type_id))
    return result.scalars().first()

async def get_device_type_by_name(db: AsyncSession, name: str) -> Optional[DeviceType]:
    result = await db.execute(select(DeviceType).filter(DeviceType.name == name))
    return result.scalars().first()

async def get_device_types(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(DeviceType)).offset(skip).limit(limit)
    return result.scalars().all()

async def create_device_type(db: AsyncSession, device_type_in: DeviceTypeCreate):
    device_type = DeviceType(name=device_type_in.name)
    db.add(device_type)
    await db.commit()
    await db.refresh(device_type)
    return device_type

async def update_device_type(db: AsyncSession, device_type_id: uuid.UUID, name: Optional[str] = None) -> Optional[DeviceType]:
    device_type = await get_device_type(db, device_type_id)
    if not device_type:
        return None
    if name:
        device_type.name = name
    await db.commit()
    await db.refresh(device_type)
    return device_type
    
async def delete_device_type(db: AsyncSession, device_type_id: uuid.UUID) -> bool:
    device_type = await get_device_type(db, device_type_id)
    if not device_type:
        return False
    await db.delete(device_type)
    await db.commit()
    return True



