from http.client import HTTPResponse
from pydoc import describe
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from .forms import UserForm
from django.shortcuts import redirect
from .models import Boost, Core, Achive

from rest_framework import viewsets
from rest_framework.decorators import api_view

from rest_framework.views import APIView
from rest_framework.response import Response

from django.http import HttpResponse
from .serializers import CoreSerializer, BoostSerializer, AchiveSerializer

@login_required
def index(request): 
    core = Core.objects.get(user=request.user) 
    boosts = Boost.objects.filter(core=core) 
     
    return render(request, 'index.html', { 
        'core': core, 
        'boosts': boosts, 
    })

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
            Boost.objects.create(core=core, price=10, power=1, name="Человек обыкновенный", describtion="Работает, если пинать" )
            Boost.objects.create(core=core, price=50, power=6, name="Новый телефон", describtion="Вычисляет все на 0.01% быстрее" )
            Boost.objects.create(core=core, price=100, power=1, type=1, name="Стиральная машинка", describtion="Майнить на ней? Ну удачи...")
            Boost.objects.create(core=core, price=500, power=3, type=1, name="Первая видюха", describtion="Стоит как золото, а пользы 0")
            Boost.objects.create(core=core, price=2000, power=10, type=1, name="Мощный компьютер", describtion="Что-то подходящее для майнинга")

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
    is_levelup = core.click()

    core.save()

    return Response({ 'core': CoreSerializer(core).data, 'is_levelup': is_levelup })   


class BoostViewSet(viewsets.ModelViewSet):  
    queryset = Boost.objects.all()  
    serializer_class = BoostSerializer
    
    def get_queryset(self): 
        core = Core.objects.get(user=self.request.user) 
        boosts = Boost.objects.filter(core=core) 
        return boosts

    def partial_update(self, request, pk):
        coins = request.data['coins'] # Получаем количество монет из тела запроса.
        boost = self.queryset.get(pk=pk)

        is_levelup = boost.levelup(coins) # Передадим количество монет в метод. Этот метод мы скоро немного подкорректируем.
        if not is_levelup:
            return Response({ "error": "Не хватает денег" })
        old_boost_stats, new_boost_stats = is_levelup

        return Response({
            "old_boost_stats": self.serializer_class(old_boost_stats).data,
            "new_boost_stats": self.serializer_class(new_boost_stats).data,
        })

class AchiveViewSet(viewsets.ModelViewSet):  
    queryset = Achive.objects.all()  
    serializer_class = AchiveSerializer
    
    def get_queryset(self): 
        core = Core.objects.get(user=self.request.user) 
        achives = Achive.objects.filter(core=core) 
        return achives

    """def partial_update(self, request, pk):
        coins = request.data['coins'] # Получаем количество монет из тела запроса.
        achive = self.queryset.get(pk=pk)

        is_levelup = achive.levelup(coins) # Передадим количество монет в метод. Этот метод мы скоро немного подкорректируем.
        if not is_levelup:
            return Response({ "error": "Не хватает денег" })
        old_boost_stats, new_boost_stats = is_levelup

        return Response({
            "old_boost_stats": self.serializer_class(old_boost_stats).data,
            "new_boost_stats": self.serializer_class(new_boost_stats).data,
        })"""


@api_view(['POST']) 
def update_coins(request): 
    coins = request.data['current_coins'] 
    core = Core.objects.get(user=request.user)
   
    is_levelup = core.click()

    if (coins>=10000 and 
    (not Boost.objects.filter(core=core).get(name="Новый телефон").achiveGet)):
        Boost.objects.filter(core=core).get(name="Новый телефон").SetTrue()
        Achive.objects.create(core=core, img='../static/img/card.png', describtion="Накоплено 10т")
    
    
    if (Boost.objects.filter(core=core).get(name="Человек обыкновенный").level == 1 and
     (not Boost.objects.filter(core=core).get(name="Человек обыкновенный").achiveGet)):
        Boost.objects.filter(core=core).get(name="Человек обыкновенный").SetTrue()
        Achive.objects.create(core=core, img='../static/img/man.png', describtion="Нанять работника")

    if (Boost.objects.filter(core=core).get(name="Стиральная машинка").level == 1
    and (not Boost.objects.filter(core=core).get(name="Стиральная машинка").achiveGet)):
        Boost.objects.filter(core=core).get(name="Стиральная машинка").SetTrue()
        Achive.objects.create(core=core, img='../static/img/washer.png', describtion="Ты серьезно купил стиралку?")

    if (Boost.objects.filter(core=core).get(name="Мощный компьютер").level == 1
    and (not Boost.objects.filter(core=core).get(name="Мощный компьютер").achiveGet)):
        Boost.objects.filter(core=core).get(name="Мощный компьютер").SetTrue()
        Achive.objects.create(core=core, img='../static/img/comp.png', describtion="Компуктер")

    core.save()

    return Response({
        'core': CoreSerializer(core).data, 
        'is_levelup': is_levelup,
    })

@api_view(['GET'])
def get_core(request):
    core = Core.objects.get(user=request.user)
    return Response({'core': CoreSerializer(core).data})