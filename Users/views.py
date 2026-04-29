from urllib import request
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from Users.serializer import RegisterSerializer,PatientProfileSerializer,DoctorProfileSerializer,SpecializationSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.conf import settings
from Users.authentication import CookieJWTAuthentication
from rest_framework.generics import ListAPIView
from .models import Specialization

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
    authentication_classes=[CookieJWTAuthentication]

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
        data=serializer.data
        data["role"]=request.user.role
        return Response(data,status=200)
    
class CookieTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')


            response.set_cookie(
                key='access_token', 
                value=access_token,
                httponly=True, 
                secure=False, 
                samesite='Lax'
            )
          
            response.set_cookie(
                key='refresh_token', 
                value=refresh_token,
                httponly=True, 
                secure=False,
                samesite='Lax'
            )
            
           

        return response

class SpecializationListView(ListAPIView):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer