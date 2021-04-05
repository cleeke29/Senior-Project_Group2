from django.db import models
from accounts.models import User

class playlist(models.Model):
    description = models.TextField()
    song_ids = models.ManyToManyField("playlist", blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)


# Create your models here.
