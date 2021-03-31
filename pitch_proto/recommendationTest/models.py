from django.db import models

# class Musicdata(models.Model):
#     acousticness = models.FloatField()
#     artists = models.TextField()
#     danceability = models.FloatField()
#     duration_ms = models.FloatField()
#     energy = models.FloatField()
#     explicit = models.FloatField()
#     id = models.TextField(primary_key=True)
#     instrumentalness = models.FloatField()
#     key = models.FloatField()
#     liveness = models.FloatField()
#     loudness = models.FloatField()
#     mode = models.FloatField()
#     name = models.TextField()
#     popularity = models.FloatField()
#     release_date = models.DateField()
#     speechiness = models.FloatField()
#     tempo = models.FloatField()
#     valence = models.FloatField()
#     year = models.IntegerField()

class preferredMusic(models.Model):
    danceabilityPreferred = models.FloatField(blank = True)
    acousticnessPreferred = models.FloatField(blank = True)
    tempoPreferred = models.FloatField(blank = True)
    lowSongId = models.TextField(null = True)
    midSongId = models.TextField(null = True)
    highSongId = models.TextField(null = True)

class holdMyData(models.Model):
    lowSongId = models.TextField()
    midSongId = models.TextField()
    highSongId = models.TextField()
