from django.urls import path
from . import views

urlpatterns = [
    path('notes_list/', views.notes_list, name='notes_list'),
]