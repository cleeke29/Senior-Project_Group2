from django.db import models
from django.contrib.postgres.fields import ArrayField

class preferredMusic(models.Model):
    danceabilityPreferred = models.FloatField(blank = True)
    acousticnessPreferred = models.FloatField(blank = True)
    tempoPreferred = models.FloatField(blank = True)
    energyPreferred = models.FloatField(blank = True)
    loudnessPreferred = models.FloatField(blank = True)
    speechinessPreferred = models.FloatField(blank = True)
    instrumentalnessPreferred = models.FloatField(blank = True)
    livenessPreferred = models.FloatField(blank = True)
    valencePreferred = models.FloatField(blank = True)
    lowSongId = models.TextField(null = True)
    midSongId = models.TextField(null = True)
    highSongId = models.TextField(null = True)

class holdMyData(models.Model):
    lowSongId = models.TextField()
    midSongId = models.TextField()
    highSongId = models.TextField()

class quickRec(models.Model):
    user_id = models.CharField(primary_key = True, max_length = 100)
    songs = ArrayField(models.TextField(null = True))

