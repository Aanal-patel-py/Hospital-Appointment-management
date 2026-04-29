from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

class User(AbstractUser):
    class Roles(models.TextChoices):
        DOCTOR="DOCTOR","Doctor"
        PATIENT="PATIENT","Patient"
    role=models.CharField(choices=Roles.choices)
    email=models.EmailField()

class Gender(models.TextChoices):
        MALE="MALE","Male"
        FEMALE="FEMALE","Female"

class Specialization(models.Model):
    type = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.type
    
class Doctor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE, related_name='doctor_profile')
    name=models.CharField(max_length=30)
    specialization=models.ManyToManyField(Specialization)
    years_of_experience=models.IntegerField()
    is_verified=models.BooleanField(default=False)
    phonenumber=PhoneNumberField()
    gender=models.CharField(choices=Gender.choices,max_length=6)

    

class Patient(models.Model):
    
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='patient_profile')
    name=models.CharField(max_length=30)
    age=models.IntegerField()
    bloodgroup=models.CharField(max_length=3)
    gender=models.CharField(choices=Gender.choices, max_length=6)
    phonenumber=PhoneNumberField()
    height=models.DecimalField(decimal_places=2,max_digits=6)
    weight=models.DecimalField(decimal_places=2,max_digits=6)
    city=models.CharField(max_length=30)
