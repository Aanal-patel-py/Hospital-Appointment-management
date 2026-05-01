import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from Users.models import User,Doctor,Patient,Specialization
import logging

logger = logging.getLogger(__name__)

@pytest.mark.django_db
def test_login_success(api_client,creds):

    response=api_client.post('/api/login/',
    {'username' :'rahul',
        'password':'123456'})
    
    assert response.status_code == 200 
    assert "access" in response.data

@pytest.mark.django_db
def test_login_failure(api_client,creds):

    response=api_client.post('/api/login/',
        {'username' :'rhul',
        'password':'123456'})
    
    assert response.status_code == 401 

@pytest.mark.django_db
def test_invalid_token(api_client):
    api_client.credentials(HTTP_AUTHORIZATION='Bearer 3NDQ1MDc1LCJpYXQiOjE3Nzc0NDIwNzUsImp0aSI6IjQwMWI4OTIyOGY5YzQ5MzQ5MzljNWNiN2U0ZDE5YjQ3IiwidXNlcl9pZCI6IjQifQ.WmDm1zJLZs5YF2rPQNewy3R0WUYFE')
    response=api_client.get('/me/')
    assert response.status_code==status.HTTP_401_UNAUTHORIZED
    assert response.data['detail']=='Given token not valid for any token type'

@pytest.mark.django_db
def test_expired_token(api_client):
    api_client.credentials(HTTP_AUTHORIZATION='Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc3NDQ1MDc1LCJpYXQiOjE3Nzc0NDIwNzUsImp0aSI6IjQwMWI4OTIyOGY5YzQ5MzQ5MzljNWNiN2U0ZDE5YjQ3IiwidXNlcl9pZCI6IjQifQ.WmDm1zJLZs5YF2rPQNewy3R0WUYFEGcW5dG902waR2g')
    response=api_client.get('/me/')
    assert response.status_code==status.HTTP_401_UNAUTHORIZED
    # logger.info(f"{response.data}")
    assert response.data['messages'][0]['message']=='Token is expired'

@pytest.mark.django_db
def test_protected_endpoints(api_client):
     
    response=api_client.get('/me/')
    assert response.status_code==status.HTTP_401_UNAUTHORIZED
    assert response.data['detail']=='Authentication credentials were not provided.'
