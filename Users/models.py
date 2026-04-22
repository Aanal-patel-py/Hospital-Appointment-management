from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

class User(AbstractUser):
    class Roles(models.TextChoices):
        DOCTOR="DOCTOR","Doctor"
        PATIENT="PATIENT","Patient"
    role=models.CharField(choices=Roles.choices,default='PATIENT')

class Gender(models.TextChoices):
        MALE="MALE","Male"
        FEMALE="FEMALE","Female"
class Specializations(models.TextChoices):
        CARDIOLOGISTS="CARDIOLOGISTS","Cardiologists"
        NEUROSURGEON="NEUROSURGEON","Neurosurgeon"
        DENTIST="DENTIST","Dentist"

class Specialization(models.Model):
     
    type=models.CharField(choices=Specializations.choices, unique=True,max_length=30)

    def __str__(self):
        return f"{self.type}" 
    
class Doctor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE, related_name='doctor_profile')
    name=models.CharField(max_length=30)
    specialization=models.ManyToManyField(Specialization)
    years_of_experience=models.IntegerField()
    is_verified=models.BooleanField(default=False)
    phonenumber=PhoneNumberField(max_length=10)
    gender=models.CharField(choices=Gender.choices)
    

class Patient(models.Model):
    
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='patient_profile')
    name=models.CharField(max_length=30)
    age=models.IntegerField()
    bloodgroup=models.CharField(max_length=2)
    gender=models.CharField(choices=Gender.choices, max_length=30)
    phonenumber=PhoneNumberField(max_length=10)
    height=models.DecimalField(decimal_places=2,max_digits=4)
    weight=models.DecimalField(decimal_places=2,max_digits=4)
    city=models.CharField(max_length=30)
