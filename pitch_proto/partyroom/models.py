from django.db import models
\
# Create your models here.
class Listening_Room(models.Model):
    dj = models.TextField()
    link_address = models.URLField()


class Room_Invite(models.Model):
    location = models.ForeignKey(
        Listening_Room, related_name='location', on_delete=models.CASCADE
    )
    from_invite = models.TextField()
    to_invite = models.TextField()
