from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializer import ScheduleSerializer
from rest_framework.response import Response
from .models import DoctorSchedule,Doctor
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view,action
from .services.schedule_service import generate_slots_for_schedule
from .permissions import IsDoctorUser
from Users.authentication import CookieJWTAuthentication 
from rest_framework_simplejwt.authentication import JWTAuthentication

class MakeScheduleViewSet(ModelViewSet):
    permission_classes=[permissions.IsAuthenticated,IsDoctorUser]
    authentication_classes=[CookieJWTAuthentication,JWTAuthentication]
    serializer_class=ScheduleSerializer
    def get_queryset(self):
        user = self.request.user
        try:
            doctor = Doctor.objects.get(user=user)
            return DoctorSchedule.objects.filter(doctor=doctor)
        except Doctor.DoesNotExist:
            return DoctorSchedule.objects.none()

    def perform_create(self, serializer): # NEEDS TO BE OVERWRITTEN AS WE NEED TO GET THE DOCTOR OBJECT AND SAVE ITS INSTANCE

        user = self.request.user
        doctor = Doctor.objects.get(user=user)
        schedule = serializer.save(doctor=doctor)
        generate_slots_for_schedule(schedule) 
        # print(user)
        # return Response(result)

    # def get_serializer_class(self):
    #     if self.action == 'create':
    #         return ScheduleSerializer




    





