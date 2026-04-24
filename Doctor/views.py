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

class MakeScheduleViewSet(ModelViewSet):
    permission_classes=[permissions.IsAuthenticated,IsDoctorUser]
    serializer_class=ScheduleSerializer
    queryset=DoctorSchedule.objects.all()

    def perform_create(self, serializer): # NEEDS TO BE OVERWRIDDEN AS WE NEED TO GET THE DOCTOR OBJECT AND SAVE ITS INSTANCE
  
        user = self.request.user
        doctor_instance = Doctor.objects.get(user=user)
        serializer.save(doctor=doctor_instance)
   
        # doc_id=self.request.data.get('doctor')
        result=generate_slots_for_schedule(doctor_instance)
        print(user)
        return Response(result)

    # def get_serializer_class(self):
    #     if self.action == 'create':
    #         return ScheduleSerializer




    





