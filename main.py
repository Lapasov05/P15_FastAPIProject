from fastapi import FastAPI, APIRouter

from admin.admin import router_admin
from auth.auth import user_register_router

app = FastAPI(title="Group")
router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Hello world"}


app.include_router(router)
app.include_router(user_register_router)
app.include_router(router_admin)
