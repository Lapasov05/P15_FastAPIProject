import os
import secrets
from datetime import datetime, timedelta

from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext

from auth.utils import generate_token, verify_token
from database import get_async_session
from models.models import user, product, user_bought_products, is_admin, role, user_saved_items

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


@user_information.post('/user-purchase')
async def user_purchase(data_id: UserSaveScheme, token: dict = Depends(verify_token),
                        session: AsyncSession = Depends(get_async_session)
                        ):
    if token is None:
        raise HTTPException(status_code=401, detail='No Registered')
    users_id = token.get('user_id')
    query = select(user_bought_products).where(user_bought_products.c.user_id == users_id).where(
        user_bought_products.c.product_id == data_id.product_id)
    checks = await session.execute(query)
    exists = bool(checks.scalar())
    if exists:
        return HTTPException(status_code=400, detail="Already bought")
    else:
        balance_query = select(user.c.balance).where(user.c.id == users_id)
        balance_result = await session.execute(balance_query)
        user_balance = balance_result.scalar()
        product_query = select(product.c.price).where(product.c.id == data_id.product_id)
        product_result = await session.execute(product_query)
        result = product_result.scalar()
        if user_balance >= result:
            updated_user = update(user).where(user.c.id == users_id).values(balance=user_balance - result)
            await session.execute(updated_user)
            eighty, twenty = (result / 100) * 80, (result / 100) * 20
            owner_id = select(product).where(product.c.id == data_id.product_id)
            query2 = await session.execute(owner_id)
            data = query2.one()
            datas = data.owner_id
            query3 = select(user.c.balance).where(user.c.id == datas)
            execute4 = await session.execute(query3)
            confirmation4 = execute4.scalar()
            final = update(user).where(user.c.id == datas).values(balance=confirmation4 + eighty)
            await session.execute(final)
            query6 = select(is_admin.c.role_id)
            data3 = await session.execute(query6)
            datas3 = data3.scalar()
            query7 = select(role.c.name).where(role.c.id == datas3)
            execute1 = await session.execute(query7)
            confirmation1 = execute1.fetchone()
            gets = str(confirmation1[0])
            if gets == 'admin':
                query4 = select(is_admin.c.user_id)
                execute2 = await session.execute(query4)
                confirmation2 = execute2.fetchone()
                son = int(confirmation2[0])
                query5 = select(user).where(user.c.id == son)
                execute5 = await session.execute(query5)
                confirmation5 = execute5.one()
                son3 = confirmation5[0]
                balance_sheet = confirmation5.balance
                final2 = update(user).where(user.c.id == son3).values(balance=balance_sheet + twenty)
                await session.execute(final2)
                await session.commit()
                return {'success': True}
        else:
            return {'success': False, 'message': "Does not enough budget to buy"}


@user_information.post('/user-save-items')
async def user_saved(data_id: UserSaveScheme, token: dict = Depends(verify_token),
                     session: AsyncSession = Depends(get_async_session)
                     ):
    if token is None:
        raise HTTPException(status_code=401, detail='No Registered')
    user_id = token.get('user_id')
    query1 = select(user_saved_items).where(user_saved_items.c.user_id == user_id).where(
        user_saved_items.c.product_id == data_id.product_id)
    user_exist = await session.execute(query1)
    exist = bool(user_exist.scalar())
    if exist:
        return {'success': 'User has already liked'}

    query = UserInDB(**dict(data_id), user_id=user_id, created_at=datetime.utcnow())
    user_data = insert(user_saved_items).values(**dict(query))
    await session.execute(user_data)
    await session.commit()
    return {'success': True}


@user_information.delete('/user-save-items')
async def delete_favorites(data_id: UserSaveScheme, token: dict = Depends(verify_token),
                           session: AsyncSession = Depends(get_async_session)
                           ):
    if token is None:
        raise HTTPException(status_code=401, detail='No Registered')
    user_id = token.get('user_id')
    delete_query = select(user_saved_items).where(
        user_saved_items.c.user_id == user_id,
        user_saved_items.c.product_id == data_id.product_id
    )
    exist_data = await session.execute(delete_query)
    exist = bool(exist_data.scalar())
    if exist:
        query = delete(user_saved_items).where(
            user_saved_items.c.user_id == user_id,
            user_saved_items.c.product_id == data_id.product_id
        )
        await session.execute(query)
        await session.commit()
        return {'success': True, 'message': 'Successfully deleted'}
    else:
        return {'success': False, 'message': 'User has not liked it yet'}
