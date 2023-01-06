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
    path('deleteroom/<str:pk>/', views.deleteRoom, name="deleteroom"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutPage, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('deletemessage/<str:pk>/', views.deleteMessage, name="deletemessage"),
    path('profile/<str:pk>/', views.userProfile, name="profile"),
    path('updateuser/', views.updateUser, name="updateuser"),
    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity")
]
