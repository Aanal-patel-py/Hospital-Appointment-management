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
class BookSlotAPIView(APIView):

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
                if slot.is_booked:
                    return Response({"error":"Slot already booked"},status=400)
                slot.is_booked=True
                slot.save()

                appointment=Appointment.objects.create(patient=patient,doctor=slot.schedule.doctor,slot=slot,status=Appointment.AppointmentStatus.PENDING)

                return Response({"message":"Appointment booked successfully","appointment_id":appointment.id},status=201)

        except slot_availability.DoesNotExist:
            return Response({"error":"Slot not found"},status=404)
        
class ConfirmAppointmentAPIView(APIView):
    permission_classes=[IsAuthenticated,IsDoctorUser]

    def patch(self,request,appointment_id):
        doctor=request.user.doctor_profile
        appointment=Appointment.objects.get(id=appointment_id,doctor=doctor)

        appointment.status=AppointmentStatus.CONFIRMED
        appointment.save()

        return Response(
            {"message":"Appointment confirmed"}
        )
    
class RejectAppointmentAPIView(APIView):
    permission_classes=[IsAuthenticated,IsDoctorUser]

    def patch(self,request,appointment_id):
        doctor=request.user.doctor_profile

        with transaction.atomic():
            appt=Appointment.objects.select_for_update().get(id=appointment_id,doctor=doctor)
            appt.status=AppointmentStatus.REJECTED
            appt.save()

            appt.slot.is_booked=False
            appt.slot.save()

        return Response(
            {"message":"Appointment rejected"}
        )