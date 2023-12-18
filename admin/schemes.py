from pydantic import BaseModel


class UserList(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    phone: str
    balance:float