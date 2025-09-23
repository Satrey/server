import uuid
from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from models.devices import DeviceManufacturer
from schemas.devices import DeviceManufacturerCreate, DeviceManufacturerUpdate


# Функции для работы с DeviceManufacturer

async def get_device_manufacturer(db: AsyncSession, manufacturer_id: uuid.UUID) -> Optional[DeviceManufacturer]:
    result = await db.execute(select(DeviceManufacturer).filter(DeviceManufacturer.id == manufacturer_id))
    return result.scalars().first()

async def get_device_manufacturer_by_name(db: AsyncSession, name: str) -> Optional[DeviceManufacturer]:
    result = await db.execute(select(DeviceManufacturer).filter(DeviceManufacturer.name == name))
    return result.scalars().first()

async def get_device_manufacturers(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[DeviceManufacturer]:
    result = await db.execute(select(DeviceManufacturer).offset(skip).limit(limit))
    return result.scalars().all()

async def create_device_manufacturer(db: AsyncSession, manufacturer_in: DeviceManufacturerCreate) -> DeviceManufacturer:
    manufacturer = DeviceManufacturer(name=manufacturer_in.name.upper())
    
    db.add(manufacturer)
    await db.commit()
    await db.refresh(manufacturer)
    return manufacturer

async def update_device_manufacturer(db: AsyncSession, manufacturer: DeviceManufacturer, manufacturer_in: DeviceManufacturerUpdate) -> DeviceManufacturer:
    if manufacturer_in.name is not None:
        manufacturer.name = manufacturer_in.name.upper()

    db.add(manufacturer)
    await db.commit()
    await db.refresh(manufacturer)
    return manufacturer

async def delete_device_manufacturer(db: AsyncSession, manufacturer: DeviceManufacturer):
    await db.delete(manufacturer)
    await db.commit()

