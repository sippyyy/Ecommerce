from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import models
from app.database import get_db,Base
from app.main import app
from app.config import settings
from app.oauth2 import create_access_token
import pytest

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.db_username}:{settings.db_password}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}_test"


engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"user_name":"testuser",
                 "password":"123456",
                 "full_name":"Test User 1",
                 "phone":"1231231231",
                 "email":"testuser@1.com",
                 "address":"Test Address 1",
                 "is_activated":True,
                 "is_seller":True
                 }
    
    res = client.post('/users/',json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user



@pytest.fixture
def token(test_user):
    return create_access_token({"user_id":test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client


@pytest.fixture
def test_products(session,test_user):
    products_data = [
        {"product_name": "name 1", "product_type": "1", "price": 15,"detail":"detail13441","quantity":2200,"image":"google.com","seller_id":test_user['id']},
        {"product_name": "name 12", "product_type": "2", "price": 88,"detail":"detail13441","quantity":22400,"image":"google.com","seller_id":test_user['id']},
        {"product_name": "name 13", "product_type": "1", "price": 156,"detail":"detail13441","quantity":22200,"image":"google.com","seller_id":test_user['id']},
    ]

    def create_products_model(post):
        return models.Products(**post)
    
    product_map = map(create_products_model,products_data)
    products = list(product_map)
    
    session.add_all(products)
    session.commit()
    
    products = session.query(models.Products).all()
    return products

@pytest.fixture
def test_order(session,test_user,test_products):
    order_data = [
        {"product_id":test_products[0].id,"order_qty":10,"user_id":test_user['id']},
        {"product_id":test_products[1].id,"order_qty":50,"user_id":test_user['id']},
        {"product_id":test_products[2].id,"order_qty":60,"user_id":test_user['id']},
    ]

    def create_order_model(order):
        return models.Orders(**order)
    
    order_map = map(create_order_model,order_data)
    orders = list(order_map)
    orders = session.query(models.Orders).all()
    return orders

@pytest.fixture
def test_cart(session,test_user,test_products):
    cart_data = [
        {"product_id":test_products[0].id,"order_qty":10,"user_id":test_user['id']},
        {"product_id":test_products[1].id,"order_qty":20,"user_id":test_user['id']},
        {"product_id":test_products[2].id,"order_qty":30,"user_id":test_user['id']},
    ]
    
    def create_model_cart(cart):
        return models.Carts(**cart)
    cart_map =map(create_model_cart,cart_data)
    carts = list(cart_map)
    carts = session.query(models.Carts).all()
    return carts
