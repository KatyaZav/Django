import re
from .forms import NoteForm
from urllib import request
from django.shortcuts import render
from django.http import HttpResponse 
from .models import Note
from .models import Pet
from django.shortcuts import redirect

def Marina(request):
    return render(request, 'marina.html',{})

def add_note(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('startPage')
        else:
            form = NoteForm()
        return render(request, 'add_note.html', {'form': form})

    if request.method == "GET":
        return render(request, "add_note.html")


#def test(request):
 #   return render(request, 'add_note.html', {})

def Pets(request):
    #pets = [f'Name: {x.name} Animal type: {x.animal} Age: {x.age};' for x in Pet.objects.all()]
    #return HttpResponse(pets)
    pets = Pet.objects.all()
    return render(request, 'pets.html', {'pets':pets})

def First(request):
    #notes = [f'{note.title}: {note.text};' for note in Note.objects.all()]
    notes = Note.objects.all()
    return render(request, 'index.html', {'notes': notes})
