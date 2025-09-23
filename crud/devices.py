import uuid
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from models.devices import Device


# Функции для работы с Device

async def get_device(db: AsyncSession, device_id: uuid.UUID) -> Optional[Device]:
    result = await db.execute(
        select(Device)
        .options(
            selectinload(Device.device_type),
            selectinload(Device.manufacturer),
            selectinload(Device.model),
            selectinload(Device.rtobject),
        )
        .filter(Device.id == device_id)
    )
    return result.scalars().first()

async def get_device_by_inventary_number(db: AsyncSession, device_inventary_number: str):
    result = await db.execute(select(Device).filter(Device.inventary_number == device_inventary_number))
    return result.scalars().first()

async def get_devices(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(Device)
        .options(
            selectinload(Device.model),
            selectinload(Device.rtobject)
        )
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def create_device(db: AsyncSession, device_in):
    # device_in: pydantic модель с inventary_number, type_id, manufacturer_id, model_id, rtobject_id (rtobject_id может быть None)
    device = Device(
        inventary_number=device_in.inventary_number,
        # type_id=device_in.type_id,
        # manufacturer_id=device_in.manufacturer_id,
        model_id=device_in.model_id,
        rtobject_id=device_in.rtobject_id,
    )

    db.add(device)
    await db.commit()
    await db.refresh(device)
    return device

async def update_device(db: AsyncSession, device: Device, device_in) -> Device:
    if device_in.inventary_number is not None:
        device.inventary_number = device_in.inventary_number
    if device_in.type_id is not None:
        device.type_id = device_in.type_id
    if device_in.manufacturer_id is not None:
        device.manufacturer_id = device_in.manufacturer_id
    if device_in.model_id is not None:
        device.model_id = device_in.model_id
    if device_in.rtobject_id is not None:
        device.rtobject_id = device_in.rtobject_id

    db.add(device)
    await db.commit()
    await db.refresh(device)
    return device

async def delete_device(db: AsyncSession, device: Device):
    await db.delete(device)
    await db.commit()





