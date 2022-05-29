from pydoc import describe
from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
from copy import copy

class Core(models.Model):
    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE)
    coins = models.IntegerField(default=0)
    click_power = models.IntegerField(default=1)
    level = models.IntegerField(default=1) 
    
    def click(self): 
        self.coins += self.click_power

        if self.coins == 1:#self.check_level_price(): 
            #self.level += 1                       
    
            return True 
        return False 
     
    def check_level_price(self):
        return (self.level*2+1) 

class Boost(models.Model): 
    core = models.ForeignKey(Core, null=False, on_delete=models.CASCADE) 
    level = models.IntegerField(default=0) 
    price = models.IntegerField(default=10) 
    power = models.IntegerField(default=1)
    name = models.TextField(default='name')
    describtion = models.TextField(default='description')

    def levelup(self):
        if self.price > self.core.coins: 
            return False

        old_boost_stats = copy(self)
        
        self.core.coins -= self.price
        self.core.click_power += self.power
        self.core.save()

        self.level += 1
        self.power *= 2
        self.price *= 2
        self.save()

        return old_boost_stats, self
