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
    rank = models.IntegerField(null=True)
    
class TournamentInfo(models.Model):
    name = models.CharField(max_length=200, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    site = models.CharField(max_length=200, null=True)
    organizer = models.CharField(max_length=200, null=True)
    is_finished = models.BooleanField(default=False)

class CurrentRoundPlayerList(models.Model):
    name = models.CharField(max_length=200)
    rating = models.IntegerField()
    pairing_no = models.IntegerField()
    score = models.FloatField()
    float_status = models.IntegerField()
    opponents = ArrayField(models.IntegerField(),null=True)
    colour_hist = ArrayField(models.IntegerField(),null=True)
    tiebreak_score = models.FloatField(null=True)
    board_number = ArrayField(models.IntegerField(),null=True)
    
class Round(models.Model):
    round_no = models.IntegerField()
    is_finished_board_order = models.BooleanField(default=False)
    
class PooledResults(models.Model):
    name = models.CharField(max_length=200)
    result = models.FloatField()
    
class ResultsHistory(models.Model):
    round = models.IntegerField(null=True)
    white_no = models.IntegerField()
    white_name = models.CharField(max_length=200)
    white_result = models.FloatField()
    black_no = models.IntegerField()
    black_name = models.CharField(max_length=200)
    black_result = models.FloatField()
    
class PickledEngine(models.Model):
    pickled_engine = models.BinaryField()