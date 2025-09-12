import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from models.user import User
from db.database import get_async_session
from schemas.user import UserRead, UserCreate, UserUpdate


import crud.user as user_crud


router = APIRouter(
    prefix='/users',
    tags=['Пользователи']
)


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserCreate, session: AsyncSession = Depends(get_async_session)):
    existing = await user_crud.get_user_by_username(session, user_in.username)
    if existing:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    user = await user_crud.create_user(session, user_in)
    print(user)
    return user


@router.get("/", response_model=List[UserRead])
async def read_users(skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_async_session)):
    users = await user_crud.get_users(session, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=UserRead)
async def read_user(user_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
    user = await user_crud.get_user(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/{user_id}", response_model=UserRead)
async def update_user(user_id: uuid.UUID, user_in: UserUpdate, session: AsyncSession = Depends(get_async_session)):
    user = await user_crud.get_user(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user = await user_crud.update_user(session, user, user_in)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
    user = await user_crud.get_user(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await user_crud.delete_user(session, user)
    return None