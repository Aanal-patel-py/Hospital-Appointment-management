from rest_framework.routers import DefaultRouter
from .views import MakeScheduleViewSet

router=DefaultRouter()
router.register('doctor',MakeScheduleViewSet)

urlpatterns = router.urls
