from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.Login.as_view(), name='login'),
    path('register/', views.Register.as_view(), name ='register'),
    path('logout/', views.user_logout, name='logout'),
    path('call_click/', views.call_click),
]