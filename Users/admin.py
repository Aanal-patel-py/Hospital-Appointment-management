from django.contrib import admin
from Users.models import Doctor, Patient,Specialization,User
from django.contrib.auth.admin import UserAdmin
# from Appointments.tasks import send_email_task

# Register your models here.

# admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display=('id','username','email','role')

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    def get_specializations(self, obj):
        return ", ".join([s.type for s in obj.specialization.all()])
    
    list_display=('id', 'name','get_specializations','years_of_experience','is_verified','phonenumber','gender')
    list_filter=('specialization','gender')


    def save_model(self, request, obj, form, change):
        
        if change and 'is_verified' in form.changed_data:
     
            old_obj = Doctor.objects.get(pk=obj.pk)
            old_verified_status = old_obj.is_verified
            new_verified_status = obj.is_verified

           
            if old_verified_status != new_verified_status:
                if new_verified_status:
                    # Verified
                    subject = 'Your account has been verified!'
                    message = 'Congratulations, your doctor profile is now verified.'
                else:
                    # Unverified
                    subject = 'Your verification status has changed'
                    message = 'Your profile is currently not verified. Please contact support.'
                
                # send_email_task(subject,message,[obj.user.email])

        
        super().save_model(request, obj, form, change)


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display=('name','age','bloodgroup','gender','phonenumber','height','weight','city')
    list_filter=('city','gender','age')


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ('id', 'type')