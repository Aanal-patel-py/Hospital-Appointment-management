# permissions.py
from rest_framework.permissions import BasePermission

class IsPatientUser(BasePermission):
  
    message = "You must be a patient to perform this action."

    def has_permission(self, request, view):
    
        return bool(request.user and request.user.is_authenticated and request.user.role=='Patient')
