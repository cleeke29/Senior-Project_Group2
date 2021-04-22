from django.db import models
from accounts.models import User
from recommender.models import Track

class playlist(models.Model):
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    songs = models.ManyToManyField(Track)
