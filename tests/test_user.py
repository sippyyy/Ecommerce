import pytest
from app.Schema.user import UserOut

def test_create_user(client):
    res = client.post('/users/',
                      json={"user_name":"testuser",
                            "password":"123456",
                            "full_name":"Test User 1",
                            "phone":"1231231231",
                            "email":"testuser@1.com",
                            "is_activated":False,
                            "is_seller":True})
    print('testing....')
    assert res.status_code == 201
    
def test_edit_user(test_user,authorized_client):
    res = authorized_client.put('/users/1',
                     json={"full_name":"Test User 1",
                           "phone":"1231231231",
                           "email":"testuser@1.com",
                           "address":"edited/address/123/HCM city",
                           "is_activated":False})
    assert res.status_code == 201
    
def test_delete_user(test_user,authorized_client):
    res = authorized_client.delete('/users/1')
    assert res.status_code == 204
    

# PASSWORD CURRENT_USER is created as 123456 from conftest file
def test_change_user_password(authorized_client,test_user):
    res = authorized_client.put('/users/password/1',
                     json={"old_password":"123456",
                           "password":"123456789"})
    assert res.status_code == 204
    
def test__wrong_old_password(authorized_client,test_user):
    res = authorized_client.put('/users/password/1',
                     json={"old_password":"wrong",
                           "password":"123456789"})
    assert res.status_code == 401
    
def test__same_old_password(authorized_client,test_user):
    res = authorized_client.put('/users/password/1',
                     json={"old_password":"123456",
                           "password":"123456"})
    assert res.status_code == 401
