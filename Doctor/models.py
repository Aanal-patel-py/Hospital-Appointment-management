from django.db import models
from datetime import time
from Users.models import Doctor

class DoctorSchedule(models.Model):
    doctor= models.ForeignKey(Doctor, on_delete=models.CASCADE)
    start_date=models.DateField(auto_now=False, auto_now_add=False)
    end_date=models.DateField(auto_now=False, auto_now_add=False)
    start_time=models.TimeField(verbose_name='starttime',default=time(10,0))
    end_time=models.TimeField(verbose_name='endtime')
    slot_duration=models.IntegerField()

    class Meta:
        unique_together=('doctor','start_date','end_date')

    def __str__(self):
        return f"{self.doctor.name}"

class slot_avaibility(models.Model):
    doctor= models.ForeignKey(Doctor,on_delete=models.CASCADE)
    date=models.DateField(auto_now=False, auto_now_add=False)
    start_time=models.TimeField(verbose_name='starttime')
    end_time=models.TimeField(verbose_name='endtime')
    is_booked=models.BooleanField()

    def __str__(self):
        return f"{self.doctor.name}"


