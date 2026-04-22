from rest_framework import serializers
from django.contrib.auth import get_user_model
from Users.models import Doctor,Patient

User=get_user_model()
class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model=User
        fields=['username','password','role']

        extra_kwargs={
            'password':{'write_only': True}
        }

    def create(self,validated_data):
        request_data=self.initial_data
        role=validated_data.get('role')
        user_data=validated_data.get('username','password','role')
        user=User.objects.create_user(user_data)

        if role=='DOCTOR':
            print(validated_data)
            doctor=Doctor.objects.create(
                user=user,
                is_verified=False,
                name=request_data.get("name"),
                years_of_experience=request_data.get("years_of_experience"),
                gender=request_data.get("gender"),
                phonenumber=request_data.get("phonenumber"),
                )
            specializations_list = request_data.get("specialization", [])
            doctor.specialization.set(specializations_list)

        if role=='PATIENT':
            Patient.objects.create(user=user,
                name=request_data.get('name'),
                age=request_data.get('age'),
                bloodgroup=request_data.get('bloodgroup'),
                gender=request_data.get('gender'),
                phonenumber=request_data.get('phonenumber'),
                height=request_data.get('height'),
                weight=request_data.get('weight'),
                city=request_data.get('city'),
                )

        return user
    
# class UserSerializer(serializers.ModelSerializer):

# class DoctorSerializer(serializers.ModelSerializer):
# class PatientSerializer(serializers.ModelSerializer):