from django.urls import path
from rooms_app import views

app_name = "rooms_app"

urlpatterns = [
    path("rooms/", view=views.RoomsList.as_view()),
    path("create_booking/", view=views.BookingCreate.as_view()),
    path("delete_booking/<int:pk>",view=views.BookingDelete.as_view())
]
