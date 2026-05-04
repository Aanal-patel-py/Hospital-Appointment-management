import pytest
import logging
from rest_framework.test import APIClient
from rest_framework import status
from Appointments.tasks import send_email_task
from Users.models import User
logger = logging.getLogger(__name__)

#"Was the task triggered?"

def test_email_triggerd_on_booking_appointment(mocker,authenticated_patient_client,schedule_made): #one is fine here , it test one emails for eah view here but if u want to add more than 1 emails in each view then assert called_once would fail and you need to use assert mock_email_task.call_count == 3
    mock_task = mocker.patch("Appointments.views.send_email_task.delay")
    client=authenticated_patient_client['client']
    slot_id=schedule_made
    response=client.patch(f'/appointments/{slot_id}/book/')

    assert response.status_code==status.HTTP_200_OK
    print(mock_task.call_args)
    mock_task.assert_called_once()

#BUT FROM ABOVE COMMENT :but better to make different tests for different email logics

def test_email_triggerd_on_confirming_appointment(mocker,authenticated_doctor_client,appointment_booked):
    
    mock_task = mocker.patch("Appointments.views.send_email_task.delay")
    appointment_id=appointment_booked
    response=authenticated_doctor_client.patch(f'/appointments/{appointment_id}/confirm/')

    assert response.status_code==200
    assert response.status_code==status.HTTP_200_OK

    print(mock_task.call_args)
    mock_task.assert_called_once()

def test_email_triggerd_on_rejecting_appointment(mocker,authenticated_doctor_client,appointment_booked):
    
    mock_task = mocker.patch("Appointments.views.send_email_task.delay")
    appointment_id=appointment_booked
    response=authenticated_doctor_client.patch(f'/appointments/{appointment_id}/confirm/')

    assert response.status_code==200
    assert response.status_code==status.HTTP_200_OK
    
    print(mock_task.call_args)
    mock_task.assert_called_once()

#When task runs, did it call Django send_mail properly?

def test_email_calling_send_mail(mocker):
    mock_send_mail = mocker.patch("Appointments.tasks.send_mail")

    send_email_task("Test Subject","Test Message",["abc@gmail.com"])

    mock_send_mail.assert_called_once()

# def test_email_on_doctor_verification(mocker,authenticated_doctor_client):

#     mock_task = mocker.patch("Users.admin.send_email_task.delay")

    
#     user = User.objects.get(username='[]')
#     user.doctor_profile.is_verified = True
#     user.doctor_profile.save()

#     mock_task.assert_called_once()


    




    



    