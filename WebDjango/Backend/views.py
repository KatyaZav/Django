from http.client import HTTPResponse
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserForm
from django.shortcuts import redirect

from rest_framework.decorators import api_view

from rest_framework.views import APIView
from rest_framework.response import Response

from django.http import HttpResponse
from .serializers import CoreSerializer

from .models import Core

@login_required
def index(request):
    core = Core.objects.get(user=request.user) # Получаем объект игры текущего пользователя 
    return render(request, 'index.html', {'core': core})

    #return HttpResponse('index page')

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


class Register(APIView):
    def get(self, request):
        form = UserForm()
        return render(request, 'register.html', {'form': form})
        
    def post(self, request):
        form = UserForm(request.POST)  
        if form.is_valid():  
            user = form.save()  
            login(request, user)  

            core = Core(user=user)  
            core.save() 
            return redirect('index') 

        return render(request, 'register.html', {'form': form})

class Login(APIView):  
    form = UserForm()  
        
    def get(self, request):
        return render(request, 'login.html', {'form': self.form})
        
    def post(self, request):
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password')) 
        if user:
            login(request, user) 
            return redirect('index')

        return render(request, 'login.html', {'form': self.form, 'invalid': True})
        
@api_view(['GET']) 
@login_required 
def call_click(request):
    core = Core.objects.get(user=request.user) 
    core.click()
    core.save() 
    
    return Response({ 'core': CoreSerializer(core).data }) 