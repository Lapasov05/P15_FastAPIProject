import os
import secrets
from datetime import datetime, timedelta

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext

from sqlalchemy import select, insert, update, delete

from auth.utils import generate_token, verify_token
from database import get_async_session
from models.models import user, user_saved_items

from auth.schemes import UserInfo, UserCreate, User_In_db, UserLogin, UserInDB, UserSaveScheme

user_register_router = APIRouter()
user_information = APIRouter()
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


@user_information.post('/user-save-items')
async def user_saved(data_id: UserSaveScheme, session: AsyncSession = Depends(get_async_session)):
    query1 = select(user_saved_items).where(user_saved_items.c.user_id == data_id.user_id).where(
        user_saved_items.c.product_id == data_id.product_id)
    user_exist = await session.execute(query1)
    exist = bool(user_exist.scalar())
    if exist:
        return {'success': 'User has already liked'}

    query = UserInDB(**dict(data_id), created_at=datetime.utcnow())
    user_data = insert(user_saved_items).values(**dict(query))
    await session.execute(user_data)
    await session.commit()
    return {'success': True}


@user_information.delete('/user-save-items')
async def delete_favorites(data_id: UserSaveScheme, session: AsyncSession = Depends(get_async_session)):
    delete_query = select(user_saved_items).where(
        user_saved_items.c.user_id == data_id.user_id,
        user_saved_items.c.product_id == data_id.product_id
    )
    exist_data = await session.execute(delete_query)
    exist = bool(exist_data.scalar())
    if exist:
        query = delete(user_saved_items).where(
            user_saved_items.c.user_id == data_id.user_id,
            user_saved_items.c.product_id == data_id.product_id
        )
        await session.execute(query)
        await session.commit()
        return {'success': True, 'message': 'Successfully deleted'}
    else:
        return {'success': False, 'message': 'User have not liked it'}

