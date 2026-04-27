from django.contrib import admin
from .models import DoctorSchedule,slot_availability

@admin.register(DoctorSchedule)
class DoctorScheduleAdmin(admin.ModelAdmin):

    list_display=('id','doctor_name','start_date','end_date','start_time','end_time','slot_duration')

    def doctor_name(self,obj): #called above and then its an object so we got obj.doc.name
        return obj.doctor.name

@admin.register(slot_availability)
class SlotAvailabilityAdmin(admin.ModelAdmin):
    list_display=('doctor_name','date','start_time','end_time','is_booked')
    ordering=('date','start_time')

    def doctor_name(self,obj): #called above and then its an object so we got obj.doc.name
        return obj.schedule.doctor.name