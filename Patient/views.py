from django.shortcuts import render
from .serializer import SlotAvailabilitySerializer,DoctorListSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from datetime import datetime
from django.db.models import Q
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
        today = datetime.now().date() 
        now_time = datetime.now().time() 
        queryset = slot_availability.objects.filter( schedule__doctor_id=doctor_id, is_booked=False ).filter( Q(date__gt=today) | Q(date=today, start_time__gt=now_time) ).select_related( "schedule", "schedule__doctor" ).order_by('date', 'start_time') 
        return queryset

class DoctorListAPIView(ListAPIView):
    model=Doctor
    serializer_class=DoctorListSerializer
    queryset=Doctor.objects.all()
    
