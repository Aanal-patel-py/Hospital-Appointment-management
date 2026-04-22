from django.contrib import admin
from Users.models import Doctor, Patient,Specialization

# Register your models here.
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    def get_specializations(self, obj):
        return ", ".join([s.name for s in obj.specializations.all()])
    list_display=('name','get_specializations','years_of_experience','is_verified','phonenumber','gender')
    list_filter=('specialization','gender')


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display=('name','age','bloodgroup','gender','phonenumber','height','weight','city')
    list_filter=('city','gender','age')
@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display=('type',)