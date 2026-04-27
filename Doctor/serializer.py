from rest_framework import serializers
from .models import DoctorSchedule,slot_avaibility
from Doctor.models import Doctor
from datetime import datetime,date
from rest_framework.validators import UniqueTogetherValidator

class ScheduleSerializer(serializers.ModelSerializer):
  
    class Meta:
        model=DoctorSchedule
        exclude=['id','doctor']
        

    def validate(self,data):
        request_data=self.initial_data
        date_format='%Y-%m-%d'
        start_date=request_data.get('start_date')
        end_date=request_data.get('end_date')
        startdate=datetime.strptime(start_date,date_format)
        enddate=datetime.strptime(end_date,date_format)
        
        doctor = Doctor.objects.get(
        user=self.context["request"].user
    )

        if request_data.get('start_time')>request_data.get('end_time'):
            raise serializers.ValidationError("starttime should not be greater than endtime")
        if start_date>end_date:
            raise serializers.ValidationError("startdate should not be greater than enddate")
        if (enddate-startdate).days >7:
            raise serializers.ValidationError("you can select the range of 7 days only")
        
        overlap_exists = DoctorSchedule.objects.filter(
            doctor=doctor,
            start_date__lte=end_date,
            end_date__gte=start_date
        ).exists()

        if overlap_exists:
            raise serializers.ValidationError(
                "This schedule overlaps with an existing schedule."
            )
        return data

