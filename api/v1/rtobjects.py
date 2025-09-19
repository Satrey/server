import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from db.database import get_async_session
from schemas.devices import RTObjectResponse, RTObjectCreate, RTObjectUpdate

import crud.rtobjects as rtobject_crud

router = APIRouter(
    prefix='/rt-objects',
    tags=['ДСО']
)

@router.post("/", response_model=RTObjectResponse, status_code=status.HTTP_201_CREATED)
async def create_rtobject(rtobject_in: RTObjectCreate, session: AsyncSession = Depends(get_async_session)):
    existing = await rtobject_crud.get_rtobject_by_number(session, rtobject_in.number)
    if existing:
        raise HTTPException(status_code=400, detail="RTObject with this number already exists")
    rtobject = await rtobject_crud.create_rtobject(session, rtobject_in)
    return rtobject

@router.get("/", response_model=List[RTObjectResponse])
async def read_rtobjects(skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_async_session)):
    rtobjects = await rtobject_crud.get_rtobjects(session, skip=skip, limit=limit)
    return rtobjects

@router.get("/{rtobject_id}", response_model=RTObjectResponse)
async def read_rtobject(rtobject_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
    rtobject = await rtobject_crud.get_rtobject(session, rtobject_id)
    if not rtobject:
        raise HTTPException(status_code=404, detail="Road Traffic Light object not found")
    return rtobject

@router.patch("/{rtobject_id}", response_model=RTObjectResponse)
async def update_rtobject(rtobject_id: uuid.UUID, rtobject_in: RTObjectUpdate, session: AsyncSession = Depends(get_async_session)):
    rtobject = await rtobject_crud.get_rtobject(session, rtobject_id)
    if not rtobject:
        raise HTTPException(status_code=404, detail="Road Traffic Light object not found")
    rtobject = await rtobject_crud.update_rtobject(session, rtobject, rtobject_in)
    return rtobject

@router.delete("/{rtobject_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_rtobject(rtobject_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
    rtobject = await rtobject_crud.get_rtobject(session, rtobject_id)
    if not rtobject:
        raise HTTPException(status_code=404, detail="Road Traffic Light object not found")
    await rtobject_crud.delete_rtobject(session, rtobject)
    return None