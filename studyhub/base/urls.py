from django.urls import path
from django.http import HttpResponse
from .views import home, room, createRoom, updateRoom, deleteRoom, loginView, logoutView, registerPage, deleteMessage, userProfile, updateUser, topicPage, activityPage

urlpatterns = [
    path('login/', loginView,name='login'),
    path('logout/', logoutView,name='logout'),
    path('register/', registerPage ,name='register'),

    path('', home, name='home'),
    path('room/<str:pk>/', room, name="room"),
    path('profile/<str:pk>/', userProfile, name="user-profile"),

    path('create-room/', createRoom, name="create-room"),
    path('update-room/<str:pk>/', updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', deleteMessage, name="delete-message"),

    path('update-user/', updateUser, name="update-user"),
    
    path('topics/', topicPage, name="topics"),
    path('activity', activityPage, name="activity"),
]
