from rest_framework import serializers
from Users.models import Doctor
from Doctor.models import slot_availability
from rest_framework.serializers import ModelSerializer

class SlotAvailabilitySerializer(serializers.ModelSerializer):
    doctor = serializers.CharField(
        read_only=True,
        source="schedule.doctor.name", 
    )
    class Meta:
        model=slot_availability
        exclude=['schedule']
        read_only_fields=['doctor','date','start_time','end_time']
   

class DoctorListSerializer(serializers.ModelSerializer):
    specialization = serializers.SlugRelatedField(
        read_only=True,
        slug_field='type',
        many=True
    )
    class Meta:
        model=Doctor     
        exclude=['user']
        read_only_fields=['name','specialization','years_of_experience','is_verfied','phonenumber','gender']
        