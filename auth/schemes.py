from pydantic import BaseModel


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    username: str
    password1: str
    password2: str
    email: str
    phone: str


class User_In_db(BaseModel):
    first_name: str
    last_name: str
    username: str
    password: str
    email: str
    phone: str


class UserInfo(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    phone: str


class UserLogin(BaseModel):
    username: str
    password: str