# permissions.py
from rest_framework.permissions import BasePermission

class IsDoctorUser(BasePermission):
  
    message = "You must be a doctor to perform this action."

    def has_permission(self, request, view):
    
        return bool(request.user and request.user.is_authenticated and request.user.role=='DOCTOR' and request.user.doctor_profile.is_verified==True)
