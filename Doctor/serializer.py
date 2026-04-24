from rest_framework import serializers
from .models import DoctorSchedule,slot_avaibility

class ScheduleSerializer(serializers.ModelSerializer):
    doctor = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model=DoctorSchedule
        fields='__all__'

    def validate(self,data):
        request_data=self.initial_data

        if request_data.get('start_time')>request_data.get('end_time'):
            raise serializers.ValidationError("starttime should not be greater than endtime")
        if request_data.get('start_date')>request_data.get('end_date'):
            raise serializers.ValidationError("startdate should not be greater than enddate")
        return data
