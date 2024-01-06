from datetime import datetime
from sqlalchemy import Table, Column, String, Integer, Text, Boolean, MetaData, TIMESTAMP, Date, ForeignKey, Float

metadata = MetaData()

user = Table(
    'user',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('first_name', String, nullable=True),
    Column('last_name', String, nullable=True),
    Column('email', String),
    Column('phone', String),
    Column('username', String),
    Column('password', String),
    Column('birth_date', Date),
    Column('balance', Float, default=10000),
    Column('registered_date', TIMESTAMP, default=datetime.utcnow),
    Column('last_login', TIMESTAMP)
)

role = Table(
    'role',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String)
)

is_admin = Table(
    'is_admin',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('role_id', Integer, ForeignKey('role.id'))
)

product = Table(
    'product',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String),
    Column('owner_id', Integer, ForeignKey('user.id')),
    Column('price', Integer, default=0),
    Column('sold_count', Integer, default=0),
    Column('category', Integer, default=0),
    Column('topic', Integer, default=0),
    Column('compatible', String),
)

user_saved_items = Table(
    'user_saved_items',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('product_id', Integer, ForeignKey('product.id')),
    Column('created_at', TIMESTAMP)
)

comment = Table(
    'comment',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('product_id', Integer, ForeignKey('product.id')),
    Column('message', Text)
)

hashtags = Table(
    'hashtags',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String),
    Column('product_id', ForeignKey('product.id'))
)

category = Table(
    'category',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String),
    Column('product_count', Integer, default=0)
)

topic = Table(

    'topic',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String),
    Column('product_count', Integer, default=0)
)


compatible = Table(
    'compatible',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String),
    Column('product_count', Integer, default=0)
)

files = Table(
    'files',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('files', String),
    Column('product_id', ForeignKey('product.id')),
    Column('hash', String)
)
