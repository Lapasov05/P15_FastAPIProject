from datetime import date

from pydantic import BaseModel


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    username: str
    password1: str
    password2: str
    email: str
    phone: str
    birth_date: date


class User_In_db(BaseModel):
    first_name: str
    last_name: str
    username: str
    password: str
    email: str
    phone: str
    birth_date: date
    balance: float


class UserInfo(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    phone: str
    balance:float



class UserLogin(BaseModel):
    username: str
    password: str


class UserSaveScheme(BaseModel):
    product_id: int


class UserInDB(BaseModel):
    user_id: int
    product_id: int
    created_at: datetime