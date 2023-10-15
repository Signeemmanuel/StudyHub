from django.urls import path
from django.http import HttpResponse
from .views import home, room

urlpatterns = [
    path('', home, name='home'),
    path('room/<str:pk>', room, name="room"),
]
