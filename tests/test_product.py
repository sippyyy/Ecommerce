import requests

def test_create_product(authorized_client, test_user):
    data = {
        "product_name": "product name 1",
        "product_type": 1,
        "price": 15,
        "detail": "detail13441",
        "quantity": 2200,
    }
    response = authorized_client.post('/products/',
                           data=data,
                           files={"image": open(r'C:\Users\cuong\Downloads\dish (1).png', 'rb')}
                           )
    
    assert response.status_code == 201
