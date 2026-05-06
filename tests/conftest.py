from rest_framework.test import APIClient
import pytest
from Users.models import User,Specialization
from Appointments.models import Appointment
from Doctor.models import slot_availability,DoctorSchedule
import logging
logger = logging.getLogger(__name__)

@pytest.fixture
def api_client():
    yield APIClient()

@pytest.fixture
def creds():
    user=User.objects.create_user(
        username='rahul',
        password='123456'
    )


@pytest.fixture
def doctor_payload():
    payload = {     
    "username": "rahul",
    "password": "123456",
    "role": "DOCTOR",
    "email":"abc@gmail.com",
    "name": "Dr Rahul",
    "years_of_experience": 10,
    "gender": "MALE",
    "phonenumber": "+919876543210",
    "specialization": [1]
    }
    return payload

@pytest.fixture
def patient_payload():
    payload = {
  "username": "Helly",
  "password": "123456",
  "email":"abc@gmail.com",
   "role": "PATIENT",
  "name": "Helly",
  "age": 25,
  "bloodgroup": "A+",
  "gender": "MALE",
  "phonenumber": "+919876543210",
  "height": "170.50",
  "weight": "65.00",
  "city": "Ahmedabad"
}
    return payload

@pytest.fixture
# @pytest.fixture(params=["admin_user", "guest_user"])
def authenticated_doctor_client(db,doctor_payload):

    client=APIClient()
    
    specialization = Specialization.objects.create(type="Cardiology")
    user_data = doctor_payload.copy()
    user_data["specialization"] = [specialization.id] 
    

    client.post('/register/', user_data,format='json')

    user = User.objects.get(username="rahul")
    user.doctor_profile.is_verified = True
    user.doctor_profile.save()


    login_response = client.post('/api/login/', {
        "username": user_data["username"],
        "password": user_data["password"]
    })
    print(login_response.data)
    # logger.info(f"{login_response.data}")

    token =login_response.data.get('access')
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    
    return {'client':client,'user':user}

@pytest.fixture
def authenticated_patient_client(db,patient_payload):
    client=APIClient()

    user_data=patient_payload

    client.post('/register/', user_data,format='json')
    user = User.objects.get(username=user_data["username"])

    login_response = client.post('/api/login/', {
        "username": user_data["username"],
        "password": user_data["password"]
    })
    print(login_response.data)
    # logger.info(f"{login_response.data}")

    token =login_response.data.get('access')
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    return  {
    "client": client,
    "user": user
    }

@pytest.fixture
def schedule_made(db,authenticated_doctor_client):
    client= authenticated_doctor_client['client']

    payload={
    "start_date": "2026-05-20",
    "end_date": "2026-05-27",
    "start_time": "10:00:00",
    "end_time": "18:00:00",
    "slot_duration": 30
    }

    response=client.post('/doctor-schedule/',payload,format="json")
    logger.info(f"{response.data}")

    
    slot_id = slot_availability.objects.values_list(
            'id', flat=True
        ).first()
    
    return slot_id

@pytest.fixture
def appointment_booked(authenticated_patient_client,schedule_made):
    slot_id=schedule_made
    client=authenticated_patient_client['client']
    response1=client.patch(f'/appointments/{slot_id}/book/')

    logger.info(f" repsonse data {response1.data}")
    appointment_id=response1.data['appointment_id']
    logger.info(f"{appointment_id}")
    # appointment_details=Appointment.objects.filter(id=1)
    # slot_id=appointment_details.slot
    # logger(f"{slot_id}")
    


    return appointment_id

    

   
    # Appointment.objects.create(doctor=1,
    #     patient=1,
    #     slot=1,
    #     feedback= None,
    #     status="pending")


