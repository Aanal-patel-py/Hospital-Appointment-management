

from .views import BookSlotAPIView,ConfirmAppointmentAPIView,RejectAppointmentAPIView
from Appointments.views import BookSlotAPIView
from django.urls import path, include



urlpatterns = [

    path("slots/<int:slot_id>/book/",BookSlotAPIView.as_view()),
    path("appointments/<int:appointment_id>/confirm/",ConfirmAppointmentAPIView.as_view()),
    path("appointments/<int:appointment_id>/reject/",RejectAppointmentAPIView.as_view()),
]
