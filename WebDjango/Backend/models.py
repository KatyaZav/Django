from email.policy import default
from pydoc import describe
from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
from copy import copy
from .constants import *

class Core(models.Model):
    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE)
    coins = models.IntegerField(default=0)
    click_power = models.IntegerField(default=1)
    level = models.IntegerField(default=1)    
    auto_click_power = models.IntegerField(default=0) 
    
    def click(self): 
        self.coins += self.click_power

        if self.coins == 1:               
            return True 
        return False 
     
    def check_level_price(self):
        return (self.level*2+1) 

class Boost(models.Model): 
    type = models.PositiveSmallIntegerField(default=0, choices=BOOST_TYPE_CHOICES)

    core = models.ForeignKey(Core, null=False, on_delete=models.CASCADE) 
    level = models.IntegerField(default=0) 
    price = models.IntegerField(default=10) 
    power = models.IntegerField(default=1)
    name = models.TextField(default='name')
    describtion = models.TextField(default='description')

    def levelup(self, current_coins):
        if self.price > self.core.coins: 
            return False

        self.core.coins -= self.price
        self.core.click_power += self.power * BOOST_TYPE_VALUES[self.type]['click_power_scale'] # Умножаем силу клика на константу.
        self.core.auto_click_power += self.power * BOOST_TYPE_VALUES[self.type]['auto_click_power_scale'] # Умножаем силу автоклика на константу.
        self.core.save()

        old_boost_values = copy(self)
        self.core.coins = current_coins - self.price

        self.level += 1
        self.power *= 2
        self.price = self.price * BOOST_TYPE_VALUES[self.type]['price_scale'] 
        self.save()

        return old_boost_values, self
  

class Achive(models.Model):
    core = models.ForeignKey(Core, null=False, on_delete=models.CASCADE) 
    img = models.TextField(default="")
    describtion = models.TextField(default="")
