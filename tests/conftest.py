from rest_framework.test import APIClient
import pytest
from Users.models import User 

@pytest.fixture()
def api_client():
    yield APIClient()

@pytest.fixture()
def creds():
    user=User.objects.create_user(
        username='rahul',
        password='123456'
    )
    
