from django.urls import path
from . import views
urlpatterns = [
    path('',views.index, name="home"),
    path('room/detail/<int:pk>/',views.DetailRoom.as_view(), name="room-details"),
    path('service/detail/<int:pk>/',views.DetailService.as_view(), name="service-details"),
    path('equipment/detail/<int:pk>/',views.DetailEquipment.as_view(), name="equipment-details"),
    path('reserver/<int:id>/<str:ressource_type>/',views.reserver, name="reserver"),
    path('my_reservations/',  views.my_reservation, name="my-reservations"),
    path("cancel_reservation/<int:reservation_id>/", views.cancel_reservation, name="cancel"),
    path('delete/<int:reservation_id>/', views.delete_reservation, name='delete_reservation'),
    path('waitlist/<str:resource_model>/<int:resource_id>/', views.add_to_waitlist, name="add-to-waitelist"),
    path("user_waitlist/",views.view_user_waitlist, name="my-waitlite")
    ]