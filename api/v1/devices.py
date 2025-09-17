import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from models.device import DeviceType
from db.database import get_async_session
from schemas.device import DeviceTypeRead, DeviceTypeCreate, DeviceTypeUpdate

import crud.device as device_crud


router = APIRouter(
    prefix='/devices',
    tags=['Devices']
)

@router.post("/type", response_model=DeviceTypeRead, status_code=status.HTTP_201_CREATED)
async def create_user(device_type_in: DeviceTypeCreate, session: AsyncSession = Depends(get_async_session)):
    existing = await device_crud.get_device_type_by_name(session, device_type_in.name)
    if existing:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    device_type = await device_crud.create_device_type(session, device_type_in)
    return device_type

