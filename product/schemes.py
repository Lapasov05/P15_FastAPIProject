from pydantic import BaseModel


class CategoryList(BaseModel):
    id: int
    name: str
    product_count: int


class CategoryAdd(BaseModel):
    name: str


class TopicList(BaseModel):
    id: int
    name: str
    product_count: int


class TopicAdd(BaseModel):
    name: str


class CompatibleList(BaseModel):
    id: int
    name: str
    product_count: int


class CompatibleAdd(BaseModel):
    name: str


class ProductAdd(BaseModel):
    name: str
    price: int
    category: int
    topic: int
    compatible: str


class ProductGet(BaseModel):
    id: int
    name: str
    price: int
    category: int
    topic: int
    compatible: str
    sold_count: int

class Product(BaseModel):
    id: int
    name: str
    price: int
    category: int
    topic: int
    compatible: list
