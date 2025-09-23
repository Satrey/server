import uuid
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from models.devices import DeviceModel
from schemas.devices import DeviceModelCreate, DeviceModelUpdate


# Функции для crud операций с DeviceModel

async def get_device_model(db: AsyncSession, model_id: uuid.UUID) -> Optional[DeviceModel]:
    result = await db.execute(select(DeviceModel).options(selectinload(DeviceModel.devices)).filter(DeviceModel.id == model_id))
    return result.scalars().first()

async def get_device_models(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(DeviceModel).offset(skip).limit(limit))
    return result.scalars().all()

async def get_device_model_by_name(db: AsyncSession, name: str) -> Optional[DeviceModel]:
    result = await db.execute(select(DeviceModel).filter(DeviceModel.name == name.upper()))
    return result.scalars().first()

async def create_device_model(db: AsyncSession, model_in: DeviceModelCreate):  # model_in — pydantic схема с name и manufacturer_id
    model = DeviceModel(name=model_in.name, manufacturer_id=model_in.manufacturer_id, device_type_id=model_in.device_type_id)

    db.add(model)
    await db.commit()
    await db.refresh(model)
    return model

async def update_device_model(db: AsyncSession, model: DeviceModel, model_in: DeviceModelUpdate) -> DeviceModel:
    if model_in.name is not None:
        model.name = model_in.name
    if model_in.manufacturer_id is not None:
        model.manufacturer_id = model_in.manufacturer_id

    db.add(model)
    await db.commit()
    await db.refresh(model)
    return model

async def delete_device_model(db: AsyncSession, model: DeviceModel):
    await db.delete(model)
    await db.commit()
