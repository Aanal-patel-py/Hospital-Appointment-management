from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializer import ScheduleSerializer
from rest_framework.response import Response
from .models import DoctorSchedule,Doctor
from rest_framework import permissions

class MakeScheduleViewSet(ModelViewSet):
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=ScheduleSerializer
    queryset=DoctorSchedule.objects.all()

    def perform_create(self, serializer): # NEEDS TO BE OVERWRIDDEN AS WE NEED TO GET THE DOCTOR OBJECT AND SAVE ITS INSTANCE
  
        user = self.request.user
        doctor_instance = Doctor.objects.get(user=user)
        serializer.save(doctor=doctor_instance)


    # def get_serializer_class(self):
    #     if self.action == 'create':
    #         return ScheduleSerializer


    # def create(self, request):

    #     serializer=self.get_serializer_class()
    
       
    #     return Response(serializer.errors,status=400)

        
