import os.path
import secrets
import zipfile
from typing import List
import aiofiles
from starlette.responses import FileResponse

from auth.utils import verify_token
from database import get_async_session
from fastapi import Depends, APIRouter, HTTPException, UploadFile
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from .schemes import CategoryAdd, CategoryList, TopicAdd, TopicList, CompatibleList, CompatibleAdd, ProductAdd, \
    ProductGet, Product
from models.models import category, product, compatible, topic, files, user

product_details = APIRouter()


@product_details.post('/category')
async def add_category(blog: CategoryAdd, token: dict = Depends(verify_token),
                       session: AsyncSession = Depends(get_async_session)):
    if token is not None:
        query = insert(category).values(**dict(blog))
        await session.execute(query)
        await session.commit()
        raise HTTPException(status_code=200, detail='Added category!')


@product_details.get('/category', response_model=List[CategoryList])
async def get_category(token: dict = Depends(verify_token),
                       session: AsyncSession = Depends(get_async_session)):
    if token is not None:
        query = select(category)
        query_category = await session.execute(query)
        query_category = query_category.all()
        return query_category


@product_details.get('/category/{blog_id}', response_model=CategoryList)
async def blog_detail(blog_id: int, token: dict = Depends(verify_token),
                      session: AsyncSession = Depends(get_async_session)):
    if token is not None:
        query = select(category).where(category.c.id == blog_id)
        blog_data = await session.execute(query)
        await session.execute(query)
        user_data = blog_data.one()
        return CategoryList(**user_data._asdict())


@product_details.post('/topic')
async def add_category(blog: TopicAdd, token: dict = Depends(verify_token),
                       session: AsyncSession = Depends(get_async_session)):
    if token is not None:
        query = insert(topic).values(**dict(blog))
        await session.execute(query)
        await session.commit()
        raise HTTPException(status_code=200, detail='Added topic!')


@product_details.get('/topic', response_model=List[TopicList])
async def get_category(token: dict = Depends(verify_token),
                       session: AsyncSession = Depends(get_async_session)):
    if token is not None:
        query = select(topic)
        query_category = await session.execute(query)
        query_category = query_category.all()
        return query_category


@product_details.get('/topic/{blog_id}', response_model=TopicList)
async def blog_detail(blog_id: int, token: dict = Depends(verify_token),
                      session: AsyncSession = Depends(get_async_session)):
    if token is not None:
        query = select(category).where(category.c.id == blog_id)
        blog_data = await session.execute(query)
        await session.execute(query)
        user_data = blog_data.one()
        return CategoryList(**user_data._asdict())


@product_details.post('/compatible')
async def add_category(blog: CompatibleAdd, token: dict = Depends(verify_token),
                       session: AsyncSession = Depends(get_async_session)):
    if token is not None:
        query = insert(compatible).values(**dict(blog))
        await session.execute(query)
        await session.commit()
        raise HTTPException(status_code=200, detail='Added compatible!')


@product_details.get('/compatible', response_model=List[CategoryList])
async def get_category(token: dict = Depends(verify_token),
                       session: AsyncSession = Depends(get_async_session)):
    if token is not None:
        query = select(category)
        query_category = await session.execute(query)
        query_category = query_category.all()
        return query_category


@product_details.get('/compatible/{blog_id}', response_model=CompatibleList)
async def blog_detail(blog_id: int, token: dict = Depends(verify_token),
                      session: AsyncSession = Depends(get_async_session)):
    if token is not None:
        query = select(category).where(category.c.id == blog_id)
        blog_data = await session.execute(query)
        await session.execute(query)
        user_data = blog_data.one()
        return CategoryList(**user_data._asdict())


@product_details.post('/upload-files')
async def upload_files(product_id: int, upload_file: UploadFile, token: dict = Depends(verify_token),
                       session: AsyncSession = Depends(get_async_session)):
    try:
        if token is not None:
            name = upload_file.filename
            out_file = f'files/products/{name}'
            if name.split('.')[-1] == 'zip':
                async with aiofiles.open(out_file, 'wb') as zipf:
                    content = await upload_file.read()
                    await zipf.write(content)
                hashcode = secrets.token_hex(32)
                query = insert(files).values(files=name, product_id=product_id, hash=hashcode)
                await session.execute(query)
                await session.commit()
                return {'success': True, 'message': 'Uploaded success!'}
            else:
                return {'success': False, 'message': 'File type is not zip!'}
    except Exception as e:
        print(f"An error occurred: {e}")
    return {'error': 'Internal Server Error'}, 500


@product_details.post('/product')
async def product_add(upload_file: UploadFile, blog: ProductAdd = Depends(), token: dict = Depends(verify_token),
                      session: AsyncSession = Depends(get_async_session)):
    user_id = token.get('user_id')
    if token is not None:
        name = upload_file.filename
        out_file = f'files/products/{name}'
        if name.split('.')[-1] == 'zip':
            async with aiofiles.open(out_file, 'wb') as zipf:
                content = await upload_file.read()
                await zipf.write(content)
            hashcode = secrets.token_hex(32)
            query = insert(product).values(owner_id=user_id, files_name=name, hashcode=hashcode, **dict(blog))
            await session.execute(query)
            await session.commit()
            return {'success': True, 'message': 'Product added!'}
        else:
            return {'success': False, 'message': 'File type is not zip!'}



@product_details.get('/product', response_model=List[ProductGet])
async def getting(token: dict = Depends(verify_token),
                  session: AsyncSession = Depends(get_async_session)):
    if token is not None:
        query = select(product)
        query_category = await session.execute(query)
        query_category = query_category.all()
        return query_category


@product_details.get('/product{blog_id}', response_model=ProductGet)
async def getting(blog_id: int, token: dict = Depends(verify_token),
                  session: AsyncSession = Depends(get_async_session)):
    if token is not None:
        query = select(product).where(product.c.id == blog_id)
        blog_data = await session.execute(query)
        await session.execute(query)
        user_data = blog_data.one()
        update_query = update(product).where(product.c.id == user_data.id).values(
            sold_count=user_data.sold_count + 1)
        update_balance_salesman = update(user).where(product.c.owner_id == user.c.id).values(
            balance=product.c.price * 0.8 + user.c.balance)
        user_id = token.get('user_id')
        update_balance_client = update(user).where(user.c.id == user_id).values(
            balance=user.c.balance - product.c.price)
        await session.execute(update_query)
        await session.execute(update_balance_client)
        await session.execute(update_balance_salesman)
        await session.commit()
        return ProductGet(**user_data._asdict())


@product_details.get('/product-user', response_model=ProductGet)
async def product_get(token: dict = Depends(verify_token),
                      session: AsyncSession = Depends(get_async_session)):
    user_id = token.get('user_id')
    if token is not None:
        query = select(product).where(owner_id=user_id)
        query_category = await session.execute(query)
        query_category = query_category.all()
        return query_category


@product_details.get('/compatible/{blog_id}', response_model=List[ProductGet])
async def blog_detail(blog_id: int, token: dict = Depends(verify_token),
                      session: AsyncSession = Depends(get_async_session)):
    if token is not None:
        query = select(product).where(category.c.id == blog_id)
        blog_data = await session.execute(query)
        await session.execute(query)
        user_data = blog_data.one()
        return CategoryList(**user_data._asdict())


@product_details.get('/download-files{blog_id}')
async def download_files(hashcode: str, token: dict = Depends(verify_token),
                         session: AsyncSession = Depends(get_async_session)):
    if token is not None:
        if hashcode is None:
            raise HTTPException(status_code=404, detail='Invalid hashcode')
        query = select(product).where(product.c.hash == hashcode)
        files__data = await session.execute(query)
        files_data = files__data.one()
        file_url = f'C:/P15_FastAPIProject/files/products/{files_data.files}'
        file_name = files_data.files
        return FileResponse(path=file_url, media_type='application/octet-stream', filename=file_name)
