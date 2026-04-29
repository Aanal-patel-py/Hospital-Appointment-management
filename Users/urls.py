from django.contrib import admin
from django.urls import path,include
from Users.views import RegisterView,MeView,CookieTokenObtainPairView,SpecializationListView

urlpatterns = [
    path('register/',RegisterView.as_view(), name='register'),
    path('me/',MeView.as_view(),name='user-profile'),
    path('api/login/',CookieTokenObtainPairView.as_view(),name='login'),
    path('specializations/', SpecializationListView.as_view(),name='specialization')
    
]