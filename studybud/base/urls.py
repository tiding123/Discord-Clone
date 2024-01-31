
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.hello, name = "home"),
    path('room/<str:pk>/', views.room, name = "room"),
    path('form/',views.createRoom),
    path('update_room/<str:pk>',views.updateRoom),
    path('delete_room/<str:pk>',views.deleteRoom),
    path('loginpage/',views.loginpage, name= "loginpage"),
    path('logout/',views.logoutUser, name= "logoutUser"),
    path('register/',views.register,name="register"),
    path('DeleteMessage/<str:pk>',views.DeleteMessage,name="DeleteMessage"),
    path('profile/<str:pk>/',views.profile,name="profile")
   
]
