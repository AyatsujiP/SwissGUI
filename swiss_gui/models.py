from django.db import models

# Create your models here.

class InitialPlayerList(models.Model):
    name = models.CharField(max_length=200)
    rating = models.IntegerField()