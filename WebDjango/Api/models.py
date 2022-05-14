from django.db import models

from unittest.util import _MAX_LENGTH

# Create your models here.
class Note(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField(max_length=1337)