from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializer import ScheduleSerializer
from rest_framework.response import Response
from .models import DoctorSchedule,Doctor
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view,action
from .services.schedule_service import generate_slots_for_schedule
from .permissions import IsDoctorUser

class MakeScheduleViewSet(ModelViewSet):
    permission_classes=[permissions.IsAuthenticated,IsDoctorUser]
    serializer_class=ScheduleSerializer
    queryset=DoctorSchedule.objects.all()

    def perform_create(self, serializer): # NEEDS TO BE OVERWRIDDEN AS WE NEED TO GET THE DOCTOR OBJECT AND SAVE ITS INSTANCE
  
        user = self.request.user
        schedule = Doctor.objects.get(user=user)
        saved_schedule=serializer.save(doctor=schedule)

        # doc_id=self.request.data.get('doctor')
        generate_slots_for_schedule(saved_schedule)
        # print(user)
        # return Response(result)

    # def get_serializer_class(self):
    #     if self.action == 'create':
    #         return ScheduleSerializer





# class MakeScheduleViewSet(ModelViewSet):
#     serializer_class = ScheduleSerializer
#     permission_classes = [
#         permissions.IsAuthenticated,
#         IsDoctorUser
#     ]

#     def get_queryset(self):
#         doctor = Doctor.objects.get(
#             user=self.request.user
#         )
#         return DoctorSchedule.objects.filter(
#             doctor=doctor
#         )


#     def perform_create(self, serializer):
#         doctor = Doctor.objects.get(
#             user=self.request.user
#         )

#         saved_schedule = serializer.save(
#             doctor=doctor
#         )

#         generate_slots_for_schedule(
#             saved_schedule
#         )


#     def perform_update(self, serializer):
#         schedule = serializer.instance

#         # remove old slots before regenerating
#         schedule.slots.all().delete()

#         updated_schedule = serializer.save()

#         generate_slots_for_schedule(
#             updated_schedule
#         )


#     def perform_destroy(self, instance):
#         # delete related slots first
#         instance.slots.all().delete()

#         instance.delete()

    







# from rest_framework.viewsets import ModelViewSet
# from rest_framework import permissions
# from .serializer import ScheduleSerializer
# from .models import DoctorSchedule
# from Users.models import Doctor
# from .permissions import IsDoctorUser
# from .services.schedule_service import generate_slots_for_schedule


# class MakeScheduleViewSet(ModelViewSet):

#     permission_classes = [
#         permissions.IsAuthenticated,
#         IsDoctorUser
#     ]

#     serializer_class = ScheduleSerializer


#     def get_queryset(self):
#         doctor = Doctor.objects.get(
#             user=self.request.user
#         )

#         return DoctorSchedule.objects.filter(
#             doctor=doctor
#         )


#     def perform_create(self, serializer):

#         user = self.request.user

#         doctor = Doctor.objects.get(
#             user=user
#         )

#         saved_schedule = serializer.save(
#             doctor=doctor
#         )

#         generate_slots_for_schedule(
#             saved_schedule
#         )


#     def perform_update(self, serializer):

#         old_schedule = serializer.instance

#         # remove old slots before regenerating
#         old_schedule.slots.all().delete()

#         updated_schedule = serializer.save()

#         generate_slots_for_schedule(
#             updated_schedule
#         )


#     def perform_destroy(self, instance):

#         # remove associated slots
#         instance.slots.all().delete()

#         instance.delete()