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
from Users.authentication import CookieJWTAuthentication

class SlotAPIView(ListAPIView):
    permission_classes=[IsAuthenticated,IsPatientUser]
    authentication_classes=[CookieJWTAuthentication]
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
    
