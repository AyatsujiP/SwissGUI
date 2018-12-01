from django.db import models
from django.contrib.postgres.fields import ArrayField
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
    opponents = ArrayField(models.IntegerField(),null=True)
    colour_hist = ArrayField(models.IntegerField(),null=True)
    tiebreak_score = models.FloatField(null=True)
    

class CurrentRoundPlayerList(models.Model):
    name = models.CharField(max_length=200)
    rating = models.IntegerField()
    pairing_no = models.IntegerField()
    score = models.FloatField()
    float_status = models.IntegerField()
    opponents = ArrayField(models.IntegerField(),null=True)
    colour_hist = ArrayField(models.IntegerField(),null=True)
    tiebreak_score = models.FloatField(null=True)
    
class Round(models.Model):
    round_no = models.IntegerField()
    
class PooledResults(models.Model):
    name = models.CharField(max_length=200)
    result = models.FloatField()