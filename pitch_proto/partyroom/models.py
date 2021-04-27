from django.db import models
\
# Create your models here.
class Listening_Room(models.Model):
    """
    This models the listening rooms available.
    """
    dj = models.TextField()
    link_address = models.URLField()
    class Meta:
        app_label = 'partyroom'


class Room_Invite(models.Model):
    """
    This models the individuals who have been invited to a partyroom
    """
    location = models.ForeignKey(
        Listening_Room, related_name='location', on_delete=models.CASCADE
    )
    from_invite = models.TextField()
    to_invite = models.TextField()

    class Meta:
        app_label = 'partyroom'
