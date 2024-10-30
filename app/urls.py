from django.urls import path
from . import views
urlpatterns = [
    path('',views.index, name="home"),
    path('room/detail/<int:pk>/',views.DetailRoom.as_view(), name="room-details"),
    path('service/detail/<int:pk>/',views.DetailService.as_view(), name="service-details"),
    path('equipment/detail/<int:pk>/',views.DetailEquipment.as_view(), name="equipment-details"),
]