import os
import secrets
from datetime import datetime, timedelta

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext

from auth.utils import generate_token, verify_token
from database import get_async_session
from models.models import user

from auth.schemes import UserInfo, UserCreate, User_In_db, UserLogin

user_register_router = APIRouter()
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


@user_register_router.post('/register', response_model=UserInfo)
async def register(user_data: UserCreate, session: AsyncSession = Depends(get_async_session)):
    if user_data.password1 == user_data.password2:
        existing_username = await session.execute(select(user).where(user.c.username == user_data.username))
        existing_email = await session.execute(select(user).where(user.c.email == user_data.email))

        if existing_username.scalar_one_or_none():
            raise HTTPException(status_code=400, detail='Username already exists!')
        if existing_email.scalar_one_or_none():
            raise HTTPException(status_code=400, detail='Email already exists!')

        password = pwd_context.hash(user_data.password1)
        user_in_db = User_In_db(**dict(user_data), password=password, registered_date=datetime.now(), balance=10000)
        user_detail = insert(user).values(**dict(user_in_db))
        await session.execute(user_detail)
        await session.commit()
        user_info = UserInfo(**dict(user_in_db))
        return dict(user_info)
    else:
        raise HTTPException(status_code=401, detail='Passwords are not same !!!')


@user_register_router.post('/login')
async def login(user_data: UserLogin, session: AsyncSession = Depends(get_async_session)):
    query = select(user).where(user.c.username == user_data.username)
    user__detail = await session.execute(query)
    try:
        user_detail = user__detail.one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail='Username or password incorrect !')
    if pwd_context.verify(user_data.password, user_detail.password):
        token = generate_token(user_detail.id)
        return token
    else:
        raise HTTPException(status_code=404, detail='Username or password incorrect !')


@user_register_router.get('/user-info', response_model=UserInfo)
async def user_info(token: dict = Depends(verify_token), session: AsyncSession = Depends(get_async_session)):
    if token is None:
        raise HTTPException(status_code=401, detail='No Registered')
    user_id = token.get('user_id')
    query = select(user).where(user.c.id == user_id)
    user__detail = await session.execute(query)
    try:
        user_data = user__detail.one()
        return UserInfo(**user_data._asdict())
    except NoResultFound:
        raise HTTPException(status_code=404, detail='User not found !!!')
