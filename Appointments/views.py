from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from Doctor.models import slot_availability
from Appointments.models import Appointment
from Patient.permissions import IsPatientUser
from rest_framework.permissions import IsAuthenticated
from Appointments.serializer import AppointmentSerializer
from Doctor.permissions import IsDoctorUser
from Appointments.models import AppointmentStatus
# from .tasks import send_email_task
from Users.authentication import CookieJWTAuthentication

class BookSlotAPIView(APIView):
    authentication_classes=[CookieJWTAuthentication]

    def get_permissions(self):
        if self.request.method == 'PATCH':
            return [IsAuthenticated(), IsPatientUser()]
        return [IsAuthenticated()]

    def get(self,request):
        user=request.user

        if user.role=="PATIENT":
            qs=Appointment.objects.filter(patient=user.patient_profile)

        elif user.role=="DOCTOR":
            qs=Appointment.objects.filter(doctor=user.doctor_profile)

        else:
            return Response({"error":"Invalid role"},status=403)

        qs=qs.select_related("patient","doctor","slot").order_by("-booked_at")
        serializer=AppointmentSerializer(qs,many=True)  
        return Response(serializer.data)

    def patch(self,request,slot_id):
        patient=request.user.patient_profile
      

        try:
            with transaction.atomic():
                slot=slot_availability.objects.select_for_update().select_related("schedule","schedule__doctor").get(id=slot_id)
                print(f"{slot_id}")
                if slot.is_booked:
                    return Response({"error":"Slot already booked"},status=400)
                slot.is_booked=True
                slot.save()

                appointment=Appointment.objects.create(patient=patient,doctor=slot.schedule.doctor,slot=slot,status=AppointmentStatus.PENDING)
                message_body=f"""Appointment request for 
                date:{appointment.slot.date}, 
                slot:{appointment.slot.start_time} to {appointment.slot.end_time} 
                patient: {appointment.patient.name}"""
                email=appointment.doctor.user.email

                # send_email_task.delay('Appointment request',message_body,[email])

                return Response({"message":"Appointment request has been sent to the doctor , please wait for confirmation email","appointment_id":appointment.id},status=201)

        except slot_availability.DoesNotExist:
            return Response({"error":"Slot not found"},status=404)
        
class ConfirmAppointmentAPIView(APIView):
    permission_classes=[IsAuthenticated,IsDoctorUser]
    authentication_classes=[CookieJWTAuthentication]

    def patch(self,request,appointment_id):
        doctor=request.user.doctor_profile
        appointment=Appointment.objects.get(id=appointment_id,doctor=doctor)

        appointment.status=AppointmentStatus.CONFIRMED
        appointment.save()
        message_body=f"""
        Your Appointment has been Confirmed for 
        doctor:{appointment.doctor.name},
        Date:{appointment.slot.date},
        Slot:{appointment.slot.start_time} to {appointment.slot.end_time} 
        please be on time , Thankyou.
        """
        email=appointment.patient.user.email
        # send_email_task.delay('Appointment Confirmed',message_body,[email])

        return Response(
            {"message":"Appointment confirmed"}
        )
    
class RejectAppointmentAPIView(APIView):
    permission_classes=[IsAuthenticated,IsDoctorUser]
    authentication_classes=[CookieJWTAuthentication]

    def patch(self,request,appointment_id):
        doctor=request.user.doctor_profile

        with transaction.atomic():
            appointment=Appointment.objects.select_for_update().get(id=appointment_id,doctor=doctor)
            appointment.status=AppointmentStatus.CANCELLED
            appointment.save()

            appointment.slot.is_booked=False
            appointment.slot.save()

            message_body=f"""
            Your Appointment has been rejected for 
            doctor:{appointment.doctor.name},
            Date:{appointment.slot.date},
            Slot:{appointment.slot.start_time} to {appointment.slot.end_time} 
            We apologize for inconvienence, please try to book another slot, Thankyou.
            """
            email=appointment.patient.user.email
            # send_email_task.delay('Appointment Rejected',message_body,[email])

        return Response(
            {"message":"Appointment rejected"}
        )