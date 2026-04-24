
from rest_framework.routers import DefaultRouter
from .views import SlotViewSet,DoctorListAPIView
from django.urls import path, include

router=DefaultRouter()
router.register('doctor-slots',SlotViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('doctor/list',DoctorListAPIView().as_view()),
]
