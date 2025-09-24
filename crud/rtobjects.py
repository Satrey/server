from typing import Optional
import uuid
from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload

from models.devices import RTObject, Device


# Функции для работы с RTObject

async def get_rtobject(db: AsyncSession, rtobject_id: uuid.UUID):
    result = await db.execute(select(RTObject)).filter(RTObject.id == rtobject_id)
    return result.scalars().first()

async def get_rtobject_by_number(db: AsyncSession, rtobject_number: int):
    result = await db.execute(select(RTObject).options(selectinload(RTObject.devices)).filter(RTObject.number == rtobject_number))
    return result.scalars().first()

async def get_rtobjects(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(RTObject).options(selectinload(RTObject.devices)).offset(skip).limit(limit))
    print(result)
    return result.scalars().all()

async def create_rtobject(db: AsyncSession, rtobject_in):  # rtobject_in с number и address
    rtobject = RTObject(number=rtobject_in.number, address=rtobject_in.address)

    db.add(rtobject)
    await db.commit()
    await db.refresh(rtobject)
    return rtobject

async def update_rtobject(db: AsyncSession, rtobject: RTObject, rtobject_in) -> RTObject:
    if rtobject_in.number is not None:
        rtobject.number = rtobject_in.number
    if rtobject_in.address is not None:
        rtobject.address = rtobject_in.address

    db.add(rtobject)
    await db.commit()
    await db.refresh(rtobject)
    return rtobject

async def delete_rtobject(db: AsyncSession, rtobject: RTObject):
    await db.delete(rtobject)
    await db.commit()
