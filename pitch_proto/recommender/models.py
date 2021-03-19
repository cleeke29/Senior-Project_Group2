from django.db import models

class Artist(models.Model):
    # artist_table_id = models.AutoField(primary_key=True)
    artist_name = models.TextField()
    artist_id = models.TextField(primary_key=True)
    artist_popularity = models.FloatField(default=None, blank=True, null=True)
    artist_genres = models.TextField(default=None, blank=True, null=True)

class Album(models.Model):
    # album_table_id = models.AutoField(primary_key=True)
    artist_name = models.TextField(default=None, blank=True, null=True)
    album_id = models.TextField(primary_key=True)
    album_name = models.TextField(default=None, blank=True, null=True)
    artist_id = models.ForeignKey(Artist, on_delete=models.CASCADE, default=None, blank=True, null=True)

class AudioFeatures(models.Model):
    # audio_features_table_id = models.AutoField(primary_key=True)
    danceability = models.FloatField()
    energy = models.FloatField()
    key = models.FloatField()
    loudness = models.FloatField()
    mode = models.FloatField()
    speechiness = models.FloatField()
    acousticness = models.FloatField()
    instrumentalness = models.FloatField()
    liveness = models.FloatField()
    valence = models.FloatField()
    tempo = models.FloatField()
    features_id = models.TextField(primary_key=True)
    duration_ms = models.IntegerField()

class Track(models.Model):
    # tracks_table_id = models.AutoField(primary_key=True)
    artists = models.TextField(default=None, blank=True, null=True)
    track_name = models.TextField(default=None, blank=True, null=True)
    track_id = models.TextField(primary_key=True)
    album_name = models.TextField(default=None, blank=True, null=True)
    explicit = models.BooleanField()
    track_popularity = models.FloatField()
    year = models.IntegerField()
    track_number = models.IntegerField(default=None, blank=True, null=True)
    # album_table_id = models.ForeignKey(Album, on_delete=models.CASCADE, default=None, blank=True, null=True)
    features_id = models.OneToOneField(AudioFeatures, on_delete=models.CASCADE, default=None, blank=True, null=True)
    # artist_table_id = models.ForeignKey(Artist, on_delete=models.CASCADE, default=None, blank=True, null=True)

class Genres(models.Model):
    # genre_table_id = models.AutoField(primary_key=True)
    genre_id = models.TextField(primary_key=True)
    # genre_name = models.TextField()

class Categories(models.Model):
    # categories_table_id = models.AutoField(primary_key=True)
    category_id = models.TextField(primary_key=True)
    category_name = models.TextField()
