
from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from .models import Appointment
from django.conf import settings


@shared_task
def send_email_task(subject,message,recipient_list):
    send_mail(
        subject=subject,
        message=message,
        from_email=None,  
        recipient_list=recipient_list,
        fail_silently=False,
    )
    print("email sent")

@shared_task
def send_appointment_reminders():
   
    now = timezone.now()
 
    target_time = now + timedelta(minutes=55)
    
   
    appointments = Appointment.objects.filter(
        slot__start_time__gte=target_time - timedelta(minutes=5),                
        slot__start_time__lte=target_time + timedelta(minutes=5),
        status='CONFIRMED'
    )

    for appt in appointments:
        
        subject_p=f"Reminder: Appointment with Dr. {appt.doctor.name}"
        message_p=f"Hi {appt.patient.name}, this is a reminder for your appointment on {appt.slot.start_time}."
        recipient_list_p=[appt.patient.user.email]
        send_email_task.delay(subject_p,message_p,recipient_list_p)

    
        subject=f"Patient Reminder: {appt.patient.name}"
        message=f"Dr. {appt.doctor.name}, you have a patient, {appt.patient.name}, scheduled in 1 hour."
        recipient_list=[appt.doctor.user.email]
        send_email_task.delay(subject,message,recipient_list)
        
        
     

# # --------------------------------------------------------------------------------------------------
# #for celery-beat
# # schedule, _ = IntervalSchedule.objects.get_or_create(every=5,period=IntervalSchedule.MINUTES,)
 
# # PeriodicTask.objects.get_or_create(name="Test Task Every 10 Seconds",
# #     defaults={
# #          "interval": schedule,
# #          "task": "appointments.tasks.test_task",
# #      }
# # )