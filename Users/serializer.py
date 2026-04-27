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

    def validate(self,data):
        role=data.get('role')
        request_data=self.initial_data
        if role=='DOCTOR':
            required_fields= ['name',
                'years_of_experience',
                'gender',
                'phonenumber']
        elif role== 'PATIENT':
            required_fields=['name',
                'age',
                'bloodgroup',
                'gender',
                'phonenumber',
                'height',
                'weight',
                'city',]
        else:
            raise serializers.ValidationError("invalid role")
        
        for fields in required_fields:
            if fields not in request_data:
                raise serializers.ValidationError("some fields are not given")
        return data

    def create(self,validated_data):
        request_data=self.initial_data
        role=validated_data.get('role')
        user_name=validated_data.get('username')
        user_password=validated_data.get('password')
        user=User.objects.create_user(user_name,password=user_password,role=role)

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
    
class PatientProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model=Patient
        fields='__all__'

class DoctorProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model=Doctor
        fields='__all__'
        extra_kwargs={
            'is_verified':{'read_only': True}
        }