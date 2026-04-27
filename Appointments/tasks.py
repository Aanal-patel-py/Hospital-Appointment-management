# appointments/tasks.py

from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_email_task(subject,message,recipient_list):
    send_mail(
        subject=subject,
        message=message,
        from_email=None,  
        recipient_list=recipient_list,
        fail_silently=False,
    )

#for celery-beat
# schedule, _ = IntervalSchedule.objects.get_or_create(every=5,period=IntervalSchedule.MINUTES,)
 
# PeriodicTask.objects.get_or_create(name="Test Task Every 10 Seconds",
#     defaults={
#          "interval": schedule,
#          "task": "appointments.tasks.test_task",
#      }
# )