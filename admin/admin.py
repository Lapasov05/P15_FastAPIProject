# from typing import List
#
# from fastapi import FastAPI, APIRouter, Depends, HTTPException
# from sqlalchemy import select
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from auth.utils import verify_token, is_admin_role
# from database import get_async_session
# from models.models import user
# from .schemes import UserList
#
# router_admin = APIRouter()
#
#
# @router_admin.get('/admin/users', response_model=List[UserList])
# async def get_users_list(token: dict = Depends(verify_token), admin: bool = Depends(is_admin_role),
#                          session: AsyncSession = Depends(get_async_session)):
#     if token is not None and admin:
#         query = select(user)
#         users_list = await session.execute(query)
#         users_list = users_list.all()
#         return users_list
#     else:
#         raise HTTPException(status_code=403, detail="Forbidden")
