from django.contrib import admin
from .models import Appointment
from Doctor.models import slot_availability

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):

    def patient_name(self,obj):
        return obj.patient.name
    def doctor_name(self,obj):
        return obj.doctor.name
    
    list_display = ('id','patient_name','doctor_name','slot','status','booked_at')
    list_filter = ('status','booked_at')
    search_fields = ('patient__name','doctor__name')
