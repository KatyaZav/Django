from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.
class Note(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField(max_length=1337)

class Pet(models.Model):
    name = models.CharField(max_length=50)
    animal = models.CharField(max_length= 50)
    age = models.IntegerField()
    
