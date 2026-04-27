# permissions.py
from rest_framework.permissions import BasePermission

class IsDoctorUser(BasePermission):
  
    message = "You must be a doctor to perform this action."

    def has_permission(self, request, view):
    
        if not request.user or not request.user.is_authenticated:
            self.message = "Authentication required"
            return False

        if request.user.role != "DOCTOR":
            self.message = "Only doctors can perform this action"
            return False

        if not request.user.doctor_profile.is_verified:
            self.message = "Your doctor account is not verified yet"
            return False

        return True