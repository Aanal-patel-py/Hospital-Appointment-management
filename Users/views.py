from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth import get_user_model
from Users.serializer import RegisterSerializer,PatientProfileSerializer,DoctorProfileSerializer

class RegisterView(APIView):
    def post(self,request):
        serializer=RegisterSerializer(data=request.data)

        if serializer.is_valid():  
            serializer.save()
            return Response(serializer.data,status=200)
        else:
            return Response(serializer.errors,status=400)
        
        
class MeView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):
        role=self.request.user.role
        serializer=None
        if role=='PATIENT':
            user=request.user.patient_profile
            serializer= PatientProfileSerializer(user) #dont pass the user as data as it is not in dictionary form but is an instance
        elif role=='DOCTOR':
            user=request.user.doctor_profile
            serializer=DoctorProfileSerializer(user)
        else:
            return Response({"detail": "Invalid role"}, status=400)
        return Response(serializer.data,status=200)
    




# {
#     "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3NzAxMDA5NSwiaWF0IjoxNzc2OTIzNjk1LCJqdGkiOiJhYzhjOTM5ZDU3NmM0ZjRhOGMwM2VlNGY5N2VlMjYwYiIsInVzZXJfaWQiOiIyMSJ9.m7O1_P7G4jNjTuWFcjdxUOvL1IPhYcv7lZZ-T0YvFUM",
#     "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc2OTIzOTk1LCJpYXQiOjE3NzY5MjM2OTUsImp0aSI6ImFlODI0NWE1NTJhOTRkZmFhM2Q5MDRlMWFiNjExYjc1IiwidXNlcl9pZCI6IjIxIn0.HemwnEr03dmr_bEjomp_4zL2h3DszY1zwwdSAF1Nwf4"
# }