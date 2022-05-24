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

@login_required
def index(request):
    return HttpResponse('index page')

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
        