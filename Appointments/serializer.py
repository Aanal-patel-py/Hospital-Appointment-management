from rest_framework import serializers
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
        READ_ONLY_FIELDS = ['patient','doctor','slot','status','booked_at']

        