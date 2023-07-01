from sqlalchemy import Column, Integer,String,Boolean,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from app.database import Base
from sqlalchemy import Float


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_name=Column(String,primary_key=False,unique=True)
    password=Column(String,primary_key=False)
    full_name=Column(String,primary_key=False,nullable=True)
    phone=Column(String,primary_key=False,unique=True,nullable=True)
    email=Column(String,primary_key=False,unique=True)
    address=Column(String,primary_key=False,nullable=True)
    is_activated=Column(Boolean,server_default="FALSE")
    created_at = Column(TIMESTAMP(timezone=True),primary_key=False,server_default=text('now()'))


class  Products(Base):
    __tablename__ = 'products'
    id=Column(Integer,primary_key=True)
    product_name=Column(String)
    product_type=Column(String)
    price=Column(Float)
    detail=Column(String)
    quantity=Column(Integer)
    image=Column(String)
