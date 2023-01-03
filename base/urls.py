from django.contrib import admin
from django.urls import path
from .import views


urlpatterns = [
    path('', views.home, name="home"),
    path('room/<str:pk>/', views.room, name="room"),
    path('createroom/', views.createroom, name="createroomname"),
    path('createmessage/', views.createmessage, name="createmessagename"),
    path('createtopic/', views.createtopic, name="createtopicname"),
    path('updateRoom/<str:pk>/', views.updateRoom, name="updateroom"),
    path('deleteroom/<str:pk>/', views.deleteRoom, name="deleteroom")
]
