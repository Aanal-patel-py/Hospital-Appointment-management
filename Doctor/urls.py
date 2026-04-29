from rest_framework.routers import DefaultRouter
from .views import MakeScheduleViewSet
from django.urls import path, include

router=DefaultRouter()
router.register('doctor-schedule',MakeScheduleViewSet,basename='doctor-schedule')

urlpatterns = [
    path('',include(router.urls)),
    # path('test/',testView),
]

