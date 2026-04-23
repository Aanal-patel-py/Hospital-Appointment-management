from django.contrib import admin
from django.urls import path,include
from Users.views import RegisterView,MeView

urlpatterns = [
    path('register/',RegisterView.as_view(), name='register'),
    path('me/',MeView.as_view(),name='user-profile'),
    
]