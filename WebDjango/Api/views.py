from django.shortcuts import render
from rest_framework.decorators import api_view

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import NoteSerializer
from .models import Note

from django.contrib.auth import login
from django.shortcuts import redirect
from Backend.forms import UserForm

class Register(APIView):
    def get(self, request):
        form = UserForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserForm(request.POST) 
        if form.is_valid(): 
            user = form.save() 
            login(request, user) 
            return redirect('index')

        return render(request, 'register.html', {'form': form})

class NoteView(APIView):
    def get(self, request):
        id = request.query_params.get("id")
        if id:
            note = Note.objects.get(pk=id)
            serializer = NoteSerializer(note) 
            return Response(serializer.data) 

        notes = Note.objects.all() 
        serializer = NoteSerializer(notes, many=True)
    
        return Response(serializer.data) 

    def post(self, request):
        title = request.data.get('title')
        text = request.data.get('text')
        note = Note.objects.create(title=title, text=text)
       
        return Response({
            "id": note.id, 
            "title": note.title, 
            "text": note.text
        })

    def put(self, request):
        id = request.data.get('id') # Получение id из тела запроса
        if not id:
            return Response({"error": 'Нету id'})

        note = Note.objects.filter(pk=id)
        if not note:
            return Response({"error": 'Нету такой заметки'})
        title = request.data.get('title')
        text = request.data.get('text')
        note.update(title=title, text=text) # Обновление заметки
       
        updated_note = Note.objects.get(pk=id) # Получение обновленной заметки
        return Response({
            "id": updated_note.id, 
            "title": updated_note.title,
            "text": updated_note.text
        })

    def delete(self, request):
        id = request.query_params.get('id') # Получение id из параметров запроса
        if not id:
            return Response({"error": 'Нету id'})
        note = Note.objects.get(pk=id) # Получение заметки
        if not note:
            return Response({"error": 'Нету такой заметки'})
        note.delete() # Удаление заметки
       
        return Response({
            "success": 'Заметка успешно удалена'
        })



@api_view(['GET'])
def notes_list(request):    
    pass
# Create your views here.
