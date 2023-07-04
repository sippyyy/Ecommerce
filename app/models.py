from sqlalchemy import Column, Integer,String,Boolean,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from app.database import Base
from sqlalchemy import Float,text

def role_default(context):
    return context.get_current_parameters()["counter"]
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
    is_seller = Column(Boolean,server_default="FALSE")

class Products(Base):
    __tablename__ = 'products'
    id=Column(Integer,primary_key=True)
    product_name=Column(String)
    product_type=Column(String)
    price=Column(Float)
    detail=Column(String)
    quantity=Column(Integer)
    image=Column(String)
    seller_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    seller_info = relationship("Users")
    
class Orders(Base):
    __tablename__ = 'orders'
    id=Column(Integer,primary_key=True)
    order_qty = Column(Integer)
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    product_id=Column(Integer,ForeignKey("products.id",ondelete="CASCADE"),nullable=False)
    created_at= Column(TIMESTAMP(timezone=True),server_default=text('now()'))
    product_detail = relationship("Products" )
