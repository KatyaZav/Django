from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('marina/', views.Marina),
    path('', views.First, name = 'startPage'),
    path('pets/', views.Pets),
    path('test/', views.add_note, name = 'add_note'),
]