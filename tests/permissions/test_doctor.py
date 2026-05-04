import pytest
import logging
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from Appointments.models import Appointment
import logging
logger = logging.getLogger(__name__)

@pytest.mark.django_db
def test_only_doctor_can_create_schedule_successfully(authenticated_doctor_client):
    
    payload={
    "start_date": "2026-05-20",
    "end_date": "2026-05-27",
    "start_time": "10:00:00",
    "end_time": "18:00:00",
    "slot_duration": 30
    }

    response=authenticated_doctor_client.post('/doctor-schedule/',payload,format="json")
    assert response.status_code==status.HTTP_201_CREATED

@pytest.mark.django_db
def test_only_doctor_can_create_schedule_failed(authenticated_doctor_client):
  
    payload={
    "start_date": "2026-05-20",
    "end_date": "2026-05-27",
    "start_time": "10:00:00",
    "slot_duration": 30
    }

    response=authenticated_doctor_client.post('/doctor-schedule/',payload,format="json")
    assert response.status_code==status.HTTP_400_BAD_REQUEST
    assert response.data['end_time'][0]=='This field is required.'

@pytest.mark.django_db
def test_start_date_lessthan_end_date_failed(authenticated_doctor_client):
     
    payload={
    "start_date": "2026-05-20",
    "end_date": "2026-04-27",
    "start_time": "10:00:00",
    "end_time": "18:00:00",
    "slot_duration": 30
    }

    response=authenticated_doctor_client.post('/doctor-schedule/',payload,format="json")
    assert response.status_code==status.HTTP_400_BAD_REQUEST
    assert response.data['non_field_errors'][0]=='End date cannot be in the past.'

@pytest.mark.django_db
def test_start_time_lessthan_end_time_failed(authenticated_doctor_client):
     
    payload={
    "start_date": "2026-05-20",
    "end_date": "2026-05-27",
    "start_time": "18:00:00",
    "end_time": "10:00:00",
    "slot_duration": 30
    }

    response=authenticated_doctor_client.post('/doctor-schedule/',payload,format="json")
    assert response.status_code==status.HTTP_400_BAD_REQUEST
    assert response.data['non_field_errors'][0]=='starttime should not be greater than endtime'

@pytest.mark.django_db
def test_only_doctor_can_confirm_appointment(appointment_booked, authenticated_doctor_client):
    appointment_id=appointment_booked

    response=authenticated_doctor_client.patch(f'/appointments/{appointment_id}/confirm/')

    assert response.status_code==200
    
    confirmed=Appointment.objects.get(id=appointment_id).status
    logger.info(f"{confirmed}")
    assert confirmed=='CONFIRMED'

@pytest.mark.django_db
def test_only_doctor_can_reject_appointment(appointment_booked,authenticated_doctor_client):
    appointment_id=appointment_booked


    response=authenticated_doctor_client.patch(f'/appointments/{appointment_id}/reject/')
    rejected=Appointment.objects.get(id=appointment_id).status
    logger.info(f"{rejected}")
    assert rejected=='CANCELLED'

    assert response.status_code==200

@pytest.mark.django_db
def test_doctor_can_see_own_appointments(authenticated_doctor_client,appointment_booked):
 

    appointment_id=appointment_booked


    response=authenticated_doctor_client.get('/appointments/')

    assert response.status_code==200
  
    assert response.data[0]['doctor']=='Dr Rahul' and response.data[0]['id']==appointment_id

    logger.info(f"data from coming doctor can see own appointments{response.data}")


@pytest.mark.django_db
def test_doctor_cannot_book_appointments(authenticated_doctor_client,schedule_made):
    slot_id=schedule_made

    response=authenticated_doctor_client.patch(f'/appointments/{slot_id}/book/')

    assert response.status_code==status.HTTP_403_FORBIDDEN
    assert response.data['detail']=='You must be a patient to perform this action.'
    

    logger.info(f" repsonse data {response.data}")
 


    