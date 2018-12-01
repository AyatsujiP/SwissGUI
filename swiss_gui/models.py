from django.db import models

# Create your models here.

class InitialPlayerList(models.Model):
    name = models.CharField(max_length=200)
    rating = models.IntegerField()
    
class ParticipatedPlayerList(models.Model):
    name = models.CharField(max_length=200)
    rating = models.IntegerField()
    pairing_no = models.IntegerField()
    score = models.FloatField()
    float_status = models.IntegerField()

class CurrentRoundPlayerList(models.Model):
    name = models.CharField(max_length=200)
    rating = models.IntegerField()
    pairing_no = models.IntegerField()
    score = models.FloatField()
    float_status = models.IntegerField()
    
class Round(models.Model):
    round_no = models.IntegerField()
    
class PooledResults(models.Model):
    name = models.CharField(max_length=200)
    result = models.FloatField()