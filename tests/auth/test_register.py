import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from Users.models import User,Doctor,Patient,Specialization
import logging

logger = logging.getLogger(__name__)


user=get_user_model

@pytest.mark.django_db
def test_patient_user_can_register_successfully(api_client):

    payload = {
        "username": "rahul",
        "password": "123456",
        "role": "PATIENT",
        "email": "rahul@gmail.com",
        "name": "Rahul",
        "age": 25,
        "bloodgroup": "A+",
        "gender": "MALE",
        "phonenumber": "+919876543210",
        "height": "170.50",
        "weight": "65.00",
        "city": "Ahmedabad"
    }

    response = api_client.post("/register/",payload,format="json")

    assert response.status_code == status.HTTP_201_CREATED
    logger.info(f"{response.data}")
    assert User.objects.filter(username='rahul').exists()


@pytest.mark.django_db
def test_doctor_user_can_register_successfully(api_client):


    payload = {
        "username": "rahul",
        "password": "123456",
        "role": "DOCTOR",
        "email": "rahul@gmail.com",
        "name": "Dr Rahul",
        "years_of_experience": 10,
        "gender": "MALE",
        "phonenumber": "+919876543210",
        "specialization": [1]
    }
    

    response = api_client.post("/register/",payload,format="json")
    assert Specialization.objects.create(type="CARDIOLOGISTS")

    assert response.status_code == status.HTTP_201_CREATED
    logger.info(f"{response.data}")
    assert User.objects.filter(username='rahul').exists()

    assert Doctor.objects.filter(name='Dr Rahul').exists()





    


    