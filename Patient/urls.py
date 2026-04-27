

from .views import SlotAPIView,DoctorListAPIView
from django.urls import path, include



urlpatterns = [

    path('doctor/list',DoctorListAPIView().as_view()),
    path("doctor-slots/<int:doctor_id>/",SlotAPIView.as_view()),

]
