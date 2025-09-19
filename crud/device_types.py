import uuid
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from models.devices import DeviceType
from schemas.devices import DeviceTypeCreate, DeviceTypeUpdate, DeviceTypeResponse


# Функции для круд операций с DeviceType

async def get_device_type(db: AsyncSession, device_type_id: uuid.UUID) -> Optional[DeviceType]:
    result = await db.execute(select(DeviceType).filter(DeviceType.id == device_type_id))
    print(result)
    return result.scalars().first()

async def get_device_type_by_name(db: AsyncSession, name: str) -> Optional[DeviceType]:
    result = await db.execute(select(DeviceType).filter(DeviceType.name == name))
    return result.scalars().first()

async def get_device_types(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(DeviceType).offset(skip).limit(limit))
    return result.scalars().all()

async def create_device_type(db: AsyncSession, device_type_in: DeviceTypeCreate):
    device_type = DeviceType(name=device_type_in.name)
    db.add(device_type)
    await db.commit()
    await db.refresh(device_type)
    return device_type

async def update_device_type(db: AsyncSession, device_type: DeviceType, device_type_in: DeviceTypeUpdate) -> DeviceType:
    if device_type_in.name is not None:
        device_type.name = device_type_in.name

    db.add(device_type)
    await db.commit()
    await db.refresh(device_type)
    return device_type
    
async def delete_device_type(db: AsyncSession, device_type: DeviceType):
    await db.delete(device_type)
    await db.commit() 
