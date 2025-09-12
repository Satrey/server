from typing import Optional
import uuid
from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from models.user import User, Profile
from schemas.user import UserCreate, UserUpdate

async def get_user(db: AsyncSession, user_id: uuid.UUID) -> Optional[User]:
    result = await db.execute(select(User).options(selectinload(User.profile)).filter(User.id == user_id))
    return result.scalars().first()

async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    result = await db.execute(select(User).options(selectinload(User.profile)).filter(User.username == username))
    return result.scalars().first()

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(User).options(selectinload(User.profile)).offset(skip).limit(limit))
    return result.scalars().all()


async def create_user(db: AsyncSession, user_in: UserCreate):
    user = User(username=user_in.username, password=user_in.password)

    if user_in.profile:
        profile = Profile(
            first_name=user_in.profile.first_name,
            sur_name=user_in.profile.sur_name,
            last_name=user_in.profile.last_name,
            email = user_in.profile.email,
            phone = user_in.profile.phone
        )
        user.profile = profile
    
    db.add(user)
    await db.commit()
    await db.refresh(user)

    user_with_profile = await db.execute(
    select(User)
    .options(selectinload(User.profile))
    .filter(User.id == user.id)
    )
    user_obj = user_with_profile.scalar_one()
    return user_obj

async def update_user(db: AsyncSession, user: User, user_in: UserUpdate) -> User:
    if user_in.username is not None:
        user.username = user_in.username
    if user_in.password is not None:
        user.password = user_in.password

    if user_in.profile:
        if user.profile is None:
            profile = Profile(user_id=user.id)
            user.profile = profile

        profile_in = user_in.profile

        if profile_in.first_name is not None:
            user.profile.first_name = profile_in.first_name
        if profile_in.sur_name is not None:
            user.profile.sur_name = profile_in.sur_name
        if profile_in.last_name is not None:
            user.profile.last_name = profile_in.last_name
        if profile_in.email is not None:
            user.profile.email = profile_in.email
        if profile_in.phone is not None:
            user.profile.phone = profile_in.phone

    db.add(user)
    await db.commit()
    await db.refresh(user)
    user_with_profile = await db.execute(
    select(User)
    .options(selectinload(User.profile))
    .filter(User.id == user.id)
    )
    user_obj = user_with_profile.scalar_one()
    return user_obj

async def delete_user(db: AsyncSession, user: User):
    await db.delete(user)
    await db.commit() 