from django.urls import path
from . import views

urlpatterns = [
    path('notes_list/', views.NoteView.as_view(), name='notes_list'),
]