import aiofiles
from fastapi import FastAPI, APIRouter, UploadFile, Depends
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.staticfiles import StaticFiles

from admin.admin import router_admin
from auth.auth import user_register_router
from auth.utils import verify_token
from database import get_async_session
from models.models import product
from product.product import product_details
from product.schemes import ProductAdd

app = FastAPI(title="Group")
router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Hello world"}


app.include_router(router)
app.include_router(user_register_router)
app.include_router(router_admin)
app.include_router(product_details)
# app.mount('/files', StaticFiles(directory='files'), 'files')