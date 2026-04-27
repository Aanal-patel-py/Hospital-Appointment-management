from django.db import models
from Users.models import Doctor, Patient
from Doctor.models import slot_availability


class AppointmentStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    CONFIRMED = "CONFIRMED", "Confirmed"
    COMPLETED = "COMPLETED", "Completed"
    CANCELLED = "CANCELLED", "Cancelled"


class Appointment(models.Model):
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,related_name="appointments")
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE,related_name="appointments")
    slot = models.OneToOneField(slot_availability,on_delete=models.CASCADE)
    status = models.CharField(max_length=20,choices=AppointmentStatus.choices,default=AppointmentStatus.PENDING)
    feedback = models.TextField(blank=True,null=True)
    booked_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient} , {self.doctor}"