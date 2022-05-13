from django.urls import path
from . import views

urlpatterns = [
    #path('notes_list/', views.notes_list, name='notes_list'),
    path('note/', views.NoteView.as_view(), name='note'),
]