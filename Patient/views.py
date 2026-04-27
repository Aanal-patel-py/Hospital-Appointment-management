from django.shortcuts import render
from .serializer import SlotAvailabilitySerializer,DoctorListSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from Doctor.models import slot_availability   
from rest_framework.decorators import api_view
from Users.models import Doctor
from rest_framework.permissions import IsAuthenticated
from .permissions import IsPatientUser

class SlotAPIView(ListAPIView):
    permission_classes=[IsAuthenticated,IsPatientUser]
    queryset=slot_availability.objects.all()
    serializer_class=SlotAvailabilitySerializer

    def get_queryset(self):

        doctor_id = self.kwargs["doctor_id"]
        if doctor_id is not None:
            queryset = slot_availability.objects.filter(schedule__doctor_id=doctor_id,is_booked=False).select_related("schedule","schedule__doctor").order_by('date','start_time')

        return queryset


class DoctorListAPIView(ListAPIView):
    model=Doctor
    serializer_class=DoctorListSerializer
    queryset=Doctor.objects.all()
    
class BookSlotAPIView(APIView):

    permission_classes = [IsAuthenticated,IsPatientUser]

    def patch(self, request, slot_id):

        try:
            slot = slot_availability.objects.get(
                id=slot_id
            )
        except slot_availability.DoesNotExist:
            return Response({"error":"Slot not found"},status=404)
        if slot.is_booked:
            return Response({"error":"Already booked"},status=400)
        slot.is_booked = True
        slot.save()
        return Response({"message":"Appointment booked"},status=200)
