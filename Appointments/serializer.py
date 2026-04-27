from rest_framework import serializers
from .models import Appointment,slot_availability

class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model=slot_availability
        fields=['date','start_time','end_time']

class AppointmentSerializer(serializers.ModelSerializer):
    slot=SlotSerializer(read_only=True)
    patient = serializers.SlugRelatedField(read_only=True,slug_field='name')
    doctor=serializers.SlugRelatedField(read_only=True,slug_field='name')
    class Meta:
        model = Appointment
        exclude=['updated_at']
        READ_ONLY_FIELDS = ['patient','doctor','slot','status','booked_at']

        