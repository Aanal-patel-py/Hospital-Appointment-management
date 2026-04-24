from rest_framework import serializers
from .models import DoctorSchedule,slot_avaibility
from datetime import datetime,date

class ScheduleSerializer(serializers.ModelSerializer):
    doctor = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model=DoctorSchedule
        fields='__all__'

    def validate(self,data):
        request_data=self.initial_data
        date_format='%Y-%m-%d'
        start_date=request_data.get('start_date')
        end_date=request_data.get('end_date')
        startdate=datetime.strptime(start_date,date_format)
        enddate=datetime.strptime(end_date,date_format)

        if request_data.get('start_time')>request_data.get('end_time'):
            raise serializers.ValidationError("starttime should not be greater than endtime")
        if start_date>end_date:
            raise serializers.ValidationError("startdate should not be greater than enddate")
        if (enddate-startdate).days >7:
            raise serializers.ValidationError("you can select the range of 7 days only")
        return data

