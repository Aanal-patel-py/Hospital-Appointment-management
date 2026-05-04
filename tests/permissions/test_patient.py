import pytest
import logging
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from Appointments.models import Appointment
import logging
logger = logging.getLogger(__name__)

@pytest.mark.django_db
def test_only_patient_can_book_appointments(authenticated_patient_client,schedule_made):
    user=authenticated_patient_client['user']
    client=authenticated_patient_client['client']
    slot_id=schedule_made
    response=client.patch(f'/appointments/{slot_id}/book/')

    logger.info(f" response data {response.data}")
    appointment_id=response.data['appointment_id']

    patient_id=Appointment.objects.get(id=appointment_id)

    assert response.status_code==status.HTTP_200_OK
    assert user.id==patient_id.patient.id
    
@pytest.mark.django_db
def test_patient_can_see_own_appointments(authenticated_patient_client,appointment_booked):
 
    client=authenticated_patient_client['client']
    appointment_id=appointment_booked

    response=client.get('/appointments/')

    assert response.status_code==status.HTTP_200_OK
    assert response.data[0]['patient']=='Helly' and response.data[0]['id']==appointment_id

    logger.info(f"{response.data}")

@pytest.mark.django_db
def test_patient_cannot_create_schedule(authenticated_patient_client):
    client=authenticated_patient_client['client']
    
    payload={
    "start_date": "2026-05-20",
    "end_date": "2026-05-27",
    "start_time": "10:00:00",
    "end_time": "18:00:00",
    "slot_duration": 30
    }

    response=client.post('/doctor-schedule/',payload,format="json")
    logger.info(f"{response.data}")
    assert response.status_code==status.HTTP_403_FORBIDDEN
    assert response.data['detail']=='Only doctors can perform this action'



