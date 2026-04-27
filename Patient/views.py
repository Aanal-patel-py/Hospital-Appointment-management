from django.shortcuts import render
from .serializer import SlotAvailabilitySerializer,DoctorListSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from Doctor.models import slot_availability   
from rest_framework.decorators import api_view
from Users.models import Doctor
from rest_framework.permissions import IsAuthenticated
from .permissions import IsPatientUser

class SlotViewSet(ModelViewSet):
    permission_classes=[IsAuthenticated,IsPatientUser]

    queryset=slot_availability.objects.all()
    serializer_class=SlotAvailabilitySerializer

    def get_queryset(self):

        queryset = slot_availability.objects.all()

        doctor_id = self.request.query_params.get('doctor')
        if doctor_id is not None:
  
            queryset = queryset.filter(doctor_id=doctor_id,is_booked=False)
        return queryset


class DoctorListAPIView(ListAPIView):
    model=Doctor
    serializer_class=DoctorListSerializer
    queryset=Doctor.objects.all()
    

