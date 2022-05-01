from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    #path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
]